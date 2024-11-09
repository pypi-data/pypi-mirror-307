from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from inferscope.models.interactive_base import InteractiveBaseModel
from inferscope.models.find_filter import BaseFindFilter


class Experiment(InteractiveBaseModel):
    class Status(StrEnum):
        DRAFT = "draft"
        ACTIVE = "active"
        FINISHED = "finished"
        FAILED = "failed"
        ARCHIVED = "archived"

    class CreateRequest(BaseModel):
        name: str = Field(min_length=1, max_length=255)
        parent_project: UUID | None = None
        description: str | None = None
        tags: list[str] | None = None

    @classmethod
    def entity_name(cls) -> str:
        return "experiment"

    model_config = ConfigDict(extra="allow")
    parent_project: UUID
    status: Status
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    tags: list[str] | None = None


class ExperimentFindFilter(BaseFindFilter):
    project_list: list[UUID] | None = None
