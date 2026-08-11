from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CatalogUpdateRecord:
    cursor: str
    payload: str


class WorkspaceCatalogRepositoryProtocol(Protocol):
    def append_update(
        self,
        *,
        user_id: int,
        payload: str,
    ) -> str: ...

    def list_updates(
        self,
        *,
        user_id: int,
        after_cursor: str | None = None,
    ) -> list[CatalogUpdateRecord]: ...
