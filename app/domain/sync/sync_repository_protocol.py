from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SyncUpdateRecord:
    cursor: str
    payload: str


class WorkspaceSyncRepositoryProtocol(Protocol):
    def append_update(
        self,
        *,
        user_id: int,
        workspace_id: str,
        payload: str,
    ) -> str: ...

    def list_updates(
        self,
        *,
        user_id: int,
        workspace_id: str,
        after_cursor: str | None = None,
    ) -> list[SyncUpdateRecord]: ...
