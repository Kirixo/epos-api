from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from pymongo import MongoClient

from app.domain.sync.sync_repository_protocol import (
    SyncUpdateRecord,
    WorkspaceSyncRepositoryProtocol,
)
from app.domain.sync.catalog_repository_protocol import (
    CatalogUpdateRecord,
    WorkspaceCatalogRepositoryProtocol,
)


class MongoWorkspaceSyncRepository(WorkspaceSyncRepositoryProtocol):
    def __init__(self, client: MongoClient[Any], database_name: str) -> None:
        self._collection = client[database_name]["workspace_sync_updates"]

    def append_update(
        self,
        *,
        user_id: int,
        workspace_id: str,
        payload: str,
    ) -> str:
        result = self._collection.insert_one(
            {
                "user_id": user_id,
                "workspace_id": workspace_id,
                "payload": payload,
                "created_at": datetime.now(UTC),
            }
        )
        return str(result.inserted_id)

    def list_updates(
        self,
        *,
        user_id: int,
        workspace_id: str,
        after_cursor: str | None = None,
    ) -> list[SyncUpdateRecord]:
        query: dict[str, object] = {
            "user_id": user_id,
            "workspace_id": workspace_id,
        }

        if after_cursor:
            query["_id"] = {"$gt": ObjectId(after_cursor)}

        docs = self._collection.find(query).sort("_id", 1)
        return [
            SyncUpdateRecord(cursor=str(doc["_id"]), payload=str(doc["payload"]))
            for doc in docs
        ]


class MongoWorkspaceCatalogRepository(WorkspaceCatalogRepositoryProtocol):
    def __init__(self, client: MongoClient[Any], database_name: str) -> None:
        self._collection = client[database_name]["workspace_catalog_updates"]

    def append_update(
        self,
        *,
        user_id: int,
        payload: str,
    ) -> str:
        result = self._collection.insert_one(
            {
                "user_id": user_id,
                "payload": payload,
                "created_at": datetime.now(UTC),
            }
        )
        return str(result.inserted_id)

    def list_updates(
        self,
        *,
        user_id: int,
        after_cursor: str | None = None,
    ) -> list[CatalogUpdateRecord]:
        query: dict[str, object] = {
            "user_id": user_id,
        }

        if after_cursor:
            query["_id"] = {"$gt": ObjectId(after_cursor)}

        docs = self._collection.find(query).sort("_id", 1)
        return [
            CatalogUpdateRecord(cursor=str(doc["_id"]), payload=str(doc["payload"]))
            for doc in docs
        ]
