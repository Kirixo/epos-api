from __future__ import annotations

from app.application.base import BaseResponse


class CatalogPushResponse(BaseResponse):
    cursor: str


class CatalogUpdateResponse(BaseResponse):
    cursor: str
    workspace_id: str
    title: str


class CatalogPullResponse(BaseResponse):
    updates: list[CatalogUpdateResponse]
