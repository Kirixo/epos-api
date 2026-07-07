from __future__ import annotations

from app.application.base import FlexibleCommand


class SyncPushCommand(FlexibleCommand):
    workspace_id: str
    payload: str


class SyncPullCommand(FlexibleCommand):
    workspace_id: str
    after_cursor: str | None = None
