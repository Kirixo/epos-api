from __future__ import annotations

from app.application.base import BaseResponse


class CatalogPushResponse(BaseResponse):
    cursor: str


class CatalogUpdateResponse(BaseResponse):
    cursor: str
    payload: str


class CatalogPullResponse(BaseResponse):
    updates: list[CatalogUpdateResponse]
