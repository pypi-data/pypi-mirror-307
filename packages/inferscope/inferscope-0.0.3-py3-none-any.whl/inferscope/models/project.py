from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from inferscope.models.find_filter import BaseFindFilter
from inferscope.models.user import UserInfo

from inferscope.models.interactive_base import InteractiveBaseModel


class Project(InteractiveBaseModel):
    class Status(StrEnum):
        ACTIVE = "active"
        ARCHIVED = "archived"

    class CreateRequest(BaseModel):
        name: str = Field(min_length=1, max_length=255)
        description: str | None = None
        tags: list[str] | None = None

    @classmethod
    def entity_name(cls) -> str:
        return "project"

    model_config = ConfigDict(extra="allow")
    status: Status
    owner: UserInfo
    members: list[UserInfo]
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    tags: list[str] | None = None


class ProjectFindFilter(BaseFindFilter):
    pass
