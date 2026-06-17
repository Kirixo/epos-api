from __future__ import annotations

from typing import Protocol

from app.domain.crud.entity import CrudEntity
from app.domain.pagination import Pagination



class CrudRepositoryProtocol(Protocol):
    def save_many(
        self,
        entities: list[CrudEntity],
    ) -> list[CrudEntity]: ...
    def save(self, *, entity: CrudEntity) -> CrudEntity: ...
    def delete(self, *, id: int) -> CrudEntity: ...
    def list(self, *, pagination: Pagination | None = None) -> list[CrudEntity]: ...
    def get(self, *, id: int) -> CrudEntity | None: ...
