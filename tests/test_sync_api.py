from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.application.sync.service import WorkspaceSyncService
from app.application.sync.catalog_service import WorkspaceCatalogSyncService
from app.domain.sync.sync_repository_protocol import (
    SyncUpdateRecord,
    WorkspaceSyncRepositoryProtocol,
)
from app.domain.sync.catalog_repository_protocol import CatalogUpdateRecord
from app.di.dependencies import get_catalog_sync_service, get_sync_service


@dataclass
class _FakeSyncStore:
    updates: list[tuple[str, int, str, str]]
    counter: int = 0

    def append_update(
        self,
        *,
        user_id: int,
        workspace_id: str,
        payload: str,
    ) -> str:
        self.counter += 1
        cursor = f"cursor-{self.counter}"
        self.updates.append((cursor, user_id, workspace_id, payload))
        return cursor

    def list_updates(
        self,
        *,
        user_id: int,
        workspace_id: str,
        after_cursor: str | None = None,
    ) -> list[SyncUpdateRecord]:
        result: list[SyncUpdateRecord] = []
        seen_cursor = after_cursor or ""
        for cursor, stored_user_id, stored_workspace_id, payload in self.updates:
            if (
                stored_user_id == user_id
                and stored_workspace_id == workspace_id
                and cursor > seen_cursor
            ):
                result.append(
                    SyncUpdateRecord(cursor=cursor, payload=payload),
                )
        return result


@dataclass
class _FakeCatalogStore:
    updates: list[tuple[str, int, str]]
    counter: int = 0

    def append_update(
        self,
        *,
        user_id: int,
        payload: str,
    ) -> str:
        self.counter += 1
        cursor = f"catalog-cursor-{self.counter}"
        self.updates.append((cursor, user_id, payload))
        return cursor

    def list_updates(
        self,
        *,
        user_id: int,
        after_cursor: str | None = None,
    ) -> list[CatalogUpdateRecord]:
        result: list[CatalogUpdateRecord] = []
        seen_cursor = after_cursor or ""
        for cursor, stored_user_id, payload in self.updates:
            if stored_user_id == user_id and cursor > seen_cursor:
                result.append(CatalogUpdateRecord(cursor=cursor, payload=payload))
        return result


@pytest.fixture()
def sync_override() -> Generator[WorkspaceSyncService, None, None]:
    store: WorkspaceSyncRepositoryProtocol = _FakeSyncStore(updates=[])
    service = WorkspaceSyncService(store)
    from app.main import app

    app.dependency_overrides[get_sync_service] = lambda: service
    yield service
    app.dependency_overrides.pop(get_sync_service, None)


@pytest.fixture()
def catalog_sync_override() -> Generator[WorkspaceCatalogSyncService, None, None]:
    store = _FakeCatalogStore(updates=[])
    service = WorkspaceCatalogSyncService(store)
    from app.main import app

    app.dependency_overrides[get_catalog_sync_service] = lambda: service
    yield service
    app.dependency_overrides.pop(get_catalog_sync_service, None)


def test_push_and_pull_sync_updates(
    client: TestClient,
    sync_override: WorkspaceSyncService,
) -> None:
    response = client.post(
        "/v1/users/register",
        json={"email": "sync_api@example.com", "password": "securepassword123"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    push_one = client.post(
        "/v1/sync/push",
        headers=headers,
        json={"workspace_id": "workspace-a", "payload": "update-a"},
    )
    assert push_one.status_code == 200
    cursor_one = push_one.json()["cursor"]

    push_two = client.post(
        "/v1/sync/push",
        headers=headers,
        json={"workspace_id": "workspace-a", "payload": "update-b"},
    )
    assert push_two.status_code == 200

    pull_all = client.get(
        "/v1/sync/pull",
        headers=headers,
        params={"workspace_id": "workspace-a"},
    )
    assert pull_all.status_code == 200
    assert [item["payload"] for item in pull_all.json()["updates"]] == [
        "update-a",
        "update-b",
    ]

    pull_delta = client.get(
        "/v1/sync/pull",
        headers=headers,
        params={"workspace_id": "workspace-a", "after_cursor": cursor_one},
    )
    assert pull_delta.status_code == 200
    assert [item["payload"] for item in pull_delta.json()["updates"]] == [
        "update-b",
    ]


def test_sync_pull_preflight_allows_configured_origin(client: TestClient) -> None:
    response = client.options(
        "/v1/sync/pull?workspace_id=workspace-a",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "GET" in response.headers["access-control-allow-methods"]
    assert "authorization" in response.headers["access-control-allow-headers"].lower()


def test_catalog_push_and_pull_sync_updates(
    client: TestClient,
    catalog_sync_override: WorkspaceCatalogSyncService,
) -> None:
    response = client.post(
        "/v1/users/register",
        json={"email": "catalog_sync_api@example.com", "password": "securepassword123"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload_one = "encrypted-catalog-update-a"
    push_one = client.post(
        "/v1/sync/catalog/push",
        headers=headers,
        json={"payload": payload_one},
    )
    assert push_one.status_code == 200
    cursor_one = push_one.json()["cursor"]

    payload_two = "encrypted-catalog-update-b"
    push_two = client.post(
        "/v1/sync/catalog/push",
        headers=headers,
        json={"payload": payload_two},
    )
    assert push_two.status_code == 200

    pull_all = client.get(
        "/v1/sync/catalog/pull",
        headers=headers,
    )
    assert pull_all.status_code == 200
    assert [item["payload"] for item in pull_all.json()["updates"]] == [
        payload_one,
        payload_two,
    ]

    pull_delta = client.get(
        "/v1/sync/catalog/pull",
        headers=headers,
        params={"after_cursor": cursor_one},
    )
    assert pull_delta.status_code == 200
    assert [item["payload"] for item in pull_delta.json()["updates"]] == [
        payload_two,
    ]
