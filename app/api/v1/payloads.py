from __future__ import annotations

from pydantic import Field

from app.api.v1.transport import TransportPayload


class WorkSpaceScopedQueryPayload(TransportPayload):
    workspace_id: int | None = None
