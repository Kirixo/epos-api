from __future__ import annotations

import json

from app.application.sync.catalog_responses import (
    CatalogPullResponse,
    CatalogPushResponse,
    CatalogUpdateResponse,
)
from app.domain.sync.catalog_repository_protocol import (
    WorkspaceCatalogRepositoryProtocol,
)


class WorkspaceCatalogSyncService:
    def __init__(self, repository: WorkspaceCatalogRepositoryProtocol) -> None:
        self._repository = repository

    def push(
        self,
        *,
        user_id: int,
        workspace_id: str,
        title: str,
    ) -> CatalogPushResponse:
        cursor = self._repository.append_update(
            user_id=user_id,
            payload=json.dumps(
                {
                    "workspace_id": workspace_id,
                    "title": title,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        )
        return CatalogPushResponse(cursor=cursor)

    def pull(
        self,
        *,
        user_id: int,
        after_cursor: str | None = None,
    ) -> CatalogPullResponse:
        updates = self._repository.list_updates(
            user_id=user_id,
            after_cursor=after_cursor,
        )

        result: list[CatalogUpdateResponse] = []
        for update in updates:
            payload = json.loads(update.payload)
            result.append(
                CatalogUpdateResponse(
                    cursor=update.cursor,
                    workspace_id=str(payload["workspace_id"]),
                    title=str(payload["title"]),
                )
            )

        return CatalogPullResponse(updates=result)
