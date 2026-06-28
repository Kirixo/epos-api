from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Any

from sqlalchemy.orm import Session

from app.domain.access.user_access_repository_protocol import UserWorkspaceAccessRepositoryProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.domain.user.user_repository_protocol import UserRepositoryProtocol
from app.domain.user.revoked_token_repository_protocol import RevokedTokenRepositoryProtocol
from app.infra.db.repositories.factory import GeneralRepositoriesFactory
from app.infra.exception import BaseInfraException



class GeneralUnitOfWork(UnitOfWorkProtocol):
    workspace_access_repo: UserWorkspaceAccessRepositoryProtocol
    user_repo: UserRepositoryProtocol
    revoked_token_repo: RevokedTokenRepositoryProtocol

    def __init__(
        self,
        session_factory: Callable[[], Session],
        repository_factory: GeneralRepositoriesFactory | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._repository_factory = repository_factory or GeneralRepositoriesFactory()
        self.session: Session | None = None

    def __enter__(self) -> "GeneralUnitOfWork":
        self.session = self._session_factory()
        if self.session is None:
            raise BaseInfraException("UoW session is not started")
        self.workspace_access_repo = self._repository_factory.workspace_access_repo(self.session)
        self.user_repo = self._repository_factory.user_repository(self.session)
        self.revoked_token_repo = self._repository_factory.revoked_token_repository(self.session)
        
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.session is not None:
                self.session.close()
                self.session = None

    def commit(self) -> None:
        if self.session is None:
            raise BaseInfraException("UoW session is not started")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            raise BaseInfraException("UoW session is not started")
        self.session.rollback()


class GeneralUnitOfWorkFactory(UnitOfWorkFactoryProtocol):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def create(self, *args: Any, **kwargs: Any) -> UnitOfWorkProtocol:
        return GeneralUnitOfWork(self._session_factory)
