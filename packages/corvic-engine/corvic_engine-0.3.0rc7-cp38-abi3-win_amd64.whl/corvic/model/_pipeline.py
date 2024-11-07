import copy
import dataclasses
import datetime
import functools
import uuid
from collections.abc import Mapping
from typing import TypeAlias

import structlog
from typing_extensions import Self

from corvic import orm, system
from corvic.model._defaults import get_default_client, get_default_room_id
from corvic.model._resource import Resource, ResourceID
from corvic.model._source import Source, SourceID
from corvic.model._wrapped_proto import WrappedProto
from corvic.result import InvalidArgumentError, NotFoundError, Ok
from corvic_generated.model.v1alpha import models_pb2
from corvic_generated.orm.v1 import pipeline_pb2

PipelineID: TypeAlias = orm.PipelineID
RoomID: TypeAlias = orm.RoomID

SpecificPipeline: TypeAlias = (
    "ChunkPdfsPipeline | OcrPdfsPipeline | SanitizeParquetPipeline"
)


_logger = structlog.get_logger()


@dataclasses.dataclass(frozen=True)
class Pipeline(WrappedProto[PipelineID, models_pb2.Pipeline]):
    """Pipelines map resources to sources."""

    @classmethod
    def _specific_pipeline_from_proto(
        cls, proto: models_pb2.Pipeline, client: system.Client
    ) -> Ok[SpecificPipeline] | InvalidArgumentError:
        if proto.pipeline_transformation.HasField("ocr_pdf"):
            return Ok(OcrPdfsPipeline(client, proto, PipelineID()))

        if proto.pipeline_transformation.HasField("chunk_pdf"):
            return Ok(ChunkPdfsPipeline(client, proto, PipelineID()))

        if proto.pipeline_transformation.HasField("sanitize_parquet"):
            return Ok(SanitizeParquetPipeline(client, proto, PipelineID()))

        return InvalidArgumentError("pipeline does not have a known implementation")

    @classmethod
    def from_id(
        cls, obj_id: PipelineID, client: system.Client | None = None
    ) -> Ok[SpecificPipeline] | NotFoundError | InvalidArgumentError:
        client = client or get_default_client()
        return cls.load_proto_for(obj_id, client).and_then(
            lambda proto: cls._specific_pipeline_from_proto(proto, client)
        )

    @classmethod
    def list(
        cls,
        limit: int | None = None,
        room_id: RoomID | None = None,
        created_before: datetime.datetime | None = None,
        client: system.Client | None = None,
    ) -> Ok[list[SpecificPipeline]] | InvalidArgumentError | NotFoundError:
        client = client or get_default_client()
        match cls.list_as_proto(orm.Pipeline, client, limit, room_id, created_before):
            case NotFoundError() | InvalidArgumentError() as err:
                return err
            case Ok(protos):
                pass
        pipelines = list[SpecificPipeline]()
        for proto in protos:
            match cls._specific_pipeline_from_proto(proto, client):
                case InvalidArgumentError() as err:
                    _logger.warning("error when listing pipelines", exc_info=err)
                case Ok(pipeline):
                    pipelines.append(pipeline)
        return Ok(pipelines)

    @property
    def room_id(self):
        return RoomID(self.proto_self.room_id)

    @property
    def name(self):
        return self.proto_self.name

    @functools.cached_property
    def inputs(self) -> Mapping[str, Resource]:
        return {
            name: Resource(self.client, proto_resource, ResourceID())
            for name, proto_resource in self.proto_self.resource_inputs.items()
        }

    @functools.cached_property
    def outputs(self) -> Mapping[str, Source]:
        return {
            name: Source(self.client, proto_source, SourceID())
            for name, proto_source in self.proto_self.source_outputs.items()
        }

    def with_name(self, name: str) -> Self:
        new_proto = copy.copy(self.proto_self)
        new_proto.name = name
        return dataclasses.replace(self, proto_self=new_proto)

    def with_input(
        self, resource: Resource | ResourceID
    ) -> Ok[Self] | NotFoundError | InvalidArgumentError:
        if isinstance(resource, ResourceID):
            match Resource.from_id(resource, self.client):
                case NotFoundError() | InvalidArgumentError() as err:
                    return err
                case Ok(obj):
                    resource = obj

        if resource.room_id != self.room_id:
            return InvalidArgumentError("cannot add inputs from other rooms")

        input_name = f"output-{uuid.uuid4()}"
        new_proto = copy.copy(self.proto_self)
        new_proto.resource_inputs[input_name].CopyFrom(resource.proto_self)

        return Ok(dataclasses.replace(self, proto_self=new_proto))


@dataclasses.dataclass(frozen=True)
class ChunkPdfsPipeline(Pipeline):
    @classmethod
    def create(
        cls,
        pipeline_name: str,
        source_name: str,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | InvalidArgumentError:
        """Create a pipeline for parsing PDFs into text chunks."""
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        match Source.create(name=source_name, client=client, room_id=room_id):
            case InvalidArgumentError() as err:
                return err
            case Ok(source):
                pass

        output_name = f"output-{uuid.uuid4()}"
        proto_pipeline = models_pb2.Pipeline(
            name=pipeline_name,
            room_id=str(room_id),
            source_outputs={output_name: source.proto_self},
            pipeline_transformation=pipeline_pb2.PipelineTransformation(
                chunk_pdf=pipeline_pb2.ChunkPdfPipelineTransformation(
                    output_name=output_name
                )
            ),
        )
        return Ok(cls(client, proto_pipeline, PipelineID()))

    @property
    def output_name(self):
        return self.proto_self.pipeline_transformation.chunk_pdf.output_name

    @property
    def output_source(self):
        return self.outputs[self.output_name]


@dataclasses.dataclass(frozen=True)
class OcrPdfsPipeline(Pipeline):
    @classmethod
    def create(
        cls,
        pipeline_name: str,
        text_source_name: str,
        relationship_source_name: str,
        image_source_name: str,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | InvalidArgumentError:
        """Create a pipeline for using OCR to process PDFs into structured sources."""
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        match Source.create(name=text_source_name, client=client, room_id=room_id):
            case InvalidArgumentError() as err:
                return err
            case Ok(text_source):
                pass
        match Source.create(
            name=relationship_source_name, client=client, room_id=room_id
        ):
            case InvalidArgumentError() as err:
                return err
            case Ok(relationship_source):
                pass
        match Source.create(name=image_source_name, client=client, room_id=room_id):
            case InvalidArgumentError() as err:
                return err
            case Ok(image_source):
                pass

        text_output_name = f"text_output-{uuid.uuid4()}"
        relationship_output_name = f"relationship_output-{uuid.uuid4()}"
        image_output_name = f"image_output-{uuid.uuid4()}"
        proto_pipeline = models_pb2.Pipeline(
            name=pipeline_name,
            room_id=str(room_id),
            source_outputs={
                text_output_name: text_source.proto_self,
                relationship_output_name: relationship_source.proto_self,
                image_output_name: image_source.proto_self,
            },
            pipeline_transformation=pipeline_pb2.PipelineTransformation(
                ocr_pdf=pipeline_pb2.OcrPdfPipelineTransformation(
                    text_output_name=text_output_name,
                    relationship_output_name=relationship_output_name,
                    image_output_name=image_output_name,
                )
            ),
        )
        return Ok(cls(client, proto_pipeline, PipelineID()))

    @property
    def text_output_name(self):
        return self.proto_self.pipeline_transformation.ocr_pdf.text_output_name

    @property
    def relantionship_output_name(self):
        return self.proto_self.pipeline_transformation.ocr_pdf.relationship_output_name

    @property
    def image_output_name(self):
        return self.proto_self.pipeline_transformation.ocr_pdf.image_output_name

    @property
    def text_output_source(self):
        return self.outputs[self.text_output_name]

    @property
    def relationship_output_source(self):
        return self.outputs[self.relantionship_output_name]

    @property
    def image_output_source(self):
        return self.outputs[self.image_output_name]


@dataclasses.dataclass(frozen=True)
class SanitizeParquetPipeline(Pipeline):
    @classmethod
    def create(
        cls,
        pipeline_name: str,
        source_name: str,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | InvalidArgumentError:
        """Create a pipeline for parsing PDFs into text chunks."""
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        match Source.create(name=source_name, client=client, room_id=room_id):
            case InvalidArgumentError() as err:
                return err
            case Ok(source):
                pass

        output_name = f"output-{uuid.uuid4()}"
        proto_pipeline = models_pb2.Pipeline(
            name=pipeline_name,
            room_id=str(room_id),
            source_outputs={output_name: source.proto_self},
            pipeline_transformation=pipeline_pb2.PipelineTransformation(
                sanitize_parquet=pipeline_pb2.SanitizeParquetPipelineTransformation(
                    output_name=output_name
                )
            ),
        )
        return Ok(cls(client, proto_pipeline, PipelineID()))

    @property
    def output_name(self):
        return self.proto_self.pipeline_transformation.sanitize_parquet.output_name

    @property
    def output_source(self):
        return self.outputs[self.output_name]
