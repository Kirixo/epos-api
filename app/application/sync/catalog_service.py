from __future__ import annotations

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
        payload: str,
    ) -> CatalogPushResponse:
        cursor = self._repository.append_update(
            user_id=user_id,
            payload=payload,
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
            result.append(
                CatalogUpdateResponse(
                    cursor=update.cursor,
                    payload=update.payload,
                )
            )

        return CatalogPullResponse(updates=result)
