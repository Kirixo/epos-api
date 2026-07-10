from __future__ import annotations

from app.api.v1.transport import TransportPayload


class CatalogPushPayload(TransportPayload):
    workspace_id: str
    title: str


class CatalogPullQueryPayload(TransportPayload):
    after_cursor: str | None = None
