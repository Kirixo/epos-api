from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FlexibleCommand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class PaginationCommand(FlexibleCommand):
    limit: int | None = Field(default=None, ge=1, le=1000)
    offset: int | None = Field(default=None, ge=0)
    search: str | None = None


JsonDict = dict[str, Any]


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)
