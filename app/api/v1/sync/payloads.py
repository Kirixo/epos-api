from __future__ import annotations

from app.api.v1.transport import TransportPayload


class SyncPushPayload(TransportPayload):
    workspace_id: str
    payload: str


class SyncPullQueryPayload(TransportPayload):
    workspace_id: str
    after_cursor: str | None = None
