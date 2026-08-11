from __future__ import annotations

from app.application.sync.responses import (
    SyncPullResponse,
    SyncPushResponse,
    SyncUpdateResponse,
)
from app.domain.sync.sync_repository_protocol import WorkspaceSyncRepositoryProtocol


class WorkspaceSyncService:
    def __init__(self, repository: WorkspaceSyncRepositoryProtocol) -> None:
        self._repository = repository

    def push(
        self,
        *,
        user_id: int,
        workspace_id: str,
        payload: str,
    ) -> SyncPushResponse:
        cursor = self._repository.append_update(
            user_id=user_id,
            workspace_id=workspace_id,
            payload=payload,
        )
        return SyncPushResponse(cursor=cursor)

    def pull(
        self,
        *,
        user_id: int,
        workspace_id: str,
        after_cursor: str | None = None,
    ) -> SyncPullResponse:
        updates = self._repository.list_updates(
            user_id=user_id,
            workspace_id=workspace_id,
            after_cursor=after_cursor,
        )

        return SyncPullResponse(
            workspace_id=workspace_id,
            updates=[
                SyncUpdateResponse(cursor=update.cursor, payload=update.payload)
                for update in updates
            ],
        )
