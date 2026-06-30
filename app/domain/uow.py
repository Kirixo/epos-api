from __future__ import annotations

from types import TracebackType
from typing import Any, Protocol

from app.domain.access.user_access_repository_protocol import UserWorkspaceAccessRepositoryProtocol
from app.domain.user.user_repository_protocol import UserRepositoryProtocol
from app.domain.user.revoked_token_repository_protocol import RevokedTokenRepositoryProtocol



class UnitOfWorkProtocol(Protocol):
    user_repo: UserRepositoryProtocol
    revoked_token_repo: RevokedTokenRepositoryProtocol
    workspace_access_repo: UserWorkspaceAccessRepositoryProtocol

    def __enter__(self) -> "UnitOfWorkProtocol": ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class UnitOfWorkFactoryProtocol(Protocol):
    def create(self, *args: Any, **kwargs: Any) -> UnitOfWorkProtocol: ...
