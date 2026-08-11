from __future__ import annotations

from app.application.base import BaseResponse


class SyncPushResponse(BaseResponse):
    cursor: str


class SyncUpdateResponse(BaseResponse):
    cursor: str
    payload: str


class SyncPullResponse(BaseResponse):
    workspace_id: str
    updates: list[SyncUpdateResponse]
