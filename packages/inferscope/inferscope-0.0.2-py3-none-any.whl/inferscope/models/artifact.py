from enum import StrEnum
from typing import Literal, List

from pydantic import BaseModel, Field

from inferscope.models.data_description import DataDescription


class ArtifactType(StrEnum):
    EXTERNAL_LINK = "external_link"


class BaseArtifact(BaseModel):
    path: str = Field(min_length=1, max_length=120)
    type: ArtifactType
    data_description: DataDescription | None = None


class ExternalLinkArtifact(BaseArtifact):
    type: Literal[ArtifactType.EXTERNAL_LINK] = ArtifactType.EXTERNAL_LINK
    uri: str


class ArtifactInstance(BaseModel):
    name: str
    version: str | None = None
    description: str | None = None


class ArtifactPack(BaseModel):
    artifacts: List[ExternalLinkArtifact] | None = None
