from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TransportPayload(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class PaginationQueryPayload(TransportPayload):
    limit: int | None = Field(default=None, ge=1, le=1000)
    offset: int | None = Field(default=None, ge=0)
    search: str | None = None
