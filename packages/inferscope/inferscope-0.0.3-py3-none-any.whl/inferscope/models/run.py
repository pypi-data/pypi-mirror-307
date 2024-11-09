from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import ConfigDict, Field

from inferscope.models.artifact import ArtifactPack
from inferscope.models.dataset import DatasetInfo
from inferscope.models.find_filter import BaseFindFilter
from inferscope.models.metric import Metrics
from inferscope.models.model import ModelInfo
from inferscope.models.interactive_base import InteractiveBaseModel


class RunStatus(StrEnum):
    DRAFT = "draft"
    RUNNING = "running"
    FAILED = "failed"
    DONE = "done"


class RunUpdateRequest(ArtifactPack, Metrics):
    name: str | None = Field(min_length=1, max_length=255, default=None)
    description: str | None = None
    status: RunStatus | None = None


class Run(InteractiveBaseModel, ArtifactPack, Metrics):
    class CreateRequest(ArtifactPack, Metrics):
        parent_project_uid: UUID | None = None

        name: str | None = Field(min_length=1, max_length=255, default=None)
        description: str | None = None
        dataset: DatasetInfo | None = None
        model: ModelInfo | None = None
        status: RunStatus = RunStatus.DONE
        tags: list[str] | None = None

        override_datetime: datetime | None = None

    model_config = ConfigDict(extra="allow")

    @classmethod
    def entity_name(cls) -> str:
        return "run"

    access_ts: datetime | None = None
    parent_project_uid: UUID | None = None
    parent_experiment_uid: UUID | None = None

    name: str | None = Field(min_length=1, max_length=255, default=None)

    dataset: DatasetInfo | None = None
    description: str | None = None
    model: ModelInfo | None = None
    status: RunStatus = RunStatus.DONE
    tags: list[str] | None = None


class RunFindFilter(BaseFindFilter):
    project_id: str | None = None
    experiment_id: str | None = None
