from datetime import datetime

from pydantic import BaseModel


class BaseFindFilter(BaseModel):
    limit: int = 100
    offset: int = 0
    created_lt: datetime | None = None
    created_gte: datetime | None = None
    tags: list[str] | None = None
