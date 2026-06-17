from __future__ import annotations

from typing import Protocol

from app.domain.access.entity import UserWorkspaceAccessEntity
from app.domain.pagination import Pagination


class UserWorkspaceAccessRepositoryProtocol(Protocol):
    def save(self, *, entity: UserWorkspaceAccessEntity) -> UserWorkspaceAccessEntity: ...
    def save_many(self, *, entities: list[UserWorkspaceAccessEntity]) -> list[UserWorkspaceAccessEntity]: ...
    def get_by_user_and_workspace(self, *, user_id: int, workspace_id: int) -> UserWorkspaceAccessEntity | None: ...
    def list_by_user_id(
        self,
        *,
        user_id: int,
        pagination: Pagination | None = None,
    ) -> list[UserWorkspaceAccessEntity]: ...
    def delete(
        self,
        *,
        user_id: int,
        app_id: int
    ) -> UserWorkspaceAccessEntity: ...
    def list_by_workspace_id(
        self,
        *,
        workspace_id: int,
        pagination: Pagination | None = None,
    ) -> list[UserWorkspaceAccessEntity]: ...