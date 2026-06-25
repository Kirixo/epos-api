from sqlalchemy.orm import Session

from app.domain.access.user_access_repository_protocol import UserWorkspaceAccessRepositoryProtocol
from app.domain.crud.crud_repository_protocol import CrudRepositoryProtocol
from app.domain.user.user_repository_protocol import UserRepositoryProtocol
from app.infra.db.repositories.user_repository import UserRepository
from app.domain.access.entity import UserWorkspaceAccessEntity
from app.domain.pagination import Pagination
from app.domain.crud.entity import CrudEntity


class DummyWorkspaceAccessRepository(UserWorkspaceAccessRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, *, entity: UserWorkspaceAccessEntity) -> UserWorkspaceAccessEntity:
        raise NotImplementedError

    def save_many(self, *, entities: list[UserWorkspaceAccessEntity]) -> list[UserWorkspaceAccessEntity]:
        raise NotImplementedError

    def get_by_user_and_workspace(self, *, user_id: int, workspace_id: int) -> UserWorkspaceAccessEntity | None:
        raise NotImplementedError

    def list_by_user_id(
        self,
        *,
        user_id: int,
        pagination: Pagination | None = None,
    ) -> list[UserWorkspaceAccessEntity]:
        raise NotImplementedError

    def delete(
        self,
        *,
        user_id: int,
        app_id: int
    ) -> UserWorkspaceAccessEntity:
        raise NotImplementedError

    def list_by_workspace_id(
        self,
        *,
        workspace_id: int,
        pagination: Pagination | None = None,
    ) -> list[UserWorkspaceAccessEntity]:
        raise NotImplementedError


class DummyCrudRepository(CrudRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save_many(
        self,
        entities: list[CrudEntity],
    ) -> list[CrudEntity]:
        raise NotImplementedError

    def save(self, *, entity: CrudEntity) -> CrudEntity:
        raise NotImplementedError

    def delete(self, *, id: int) -> CrudEntity:
        raise NotImplementedError

    def list(self, *, pagination: Pagination | None = None) -> list[CrudEntity]:
        raise NotImplementedError

    def get(self, *, id: int) -> CrudEntity | None:
        raise NotImplementedError


class GeneralRepositoriesFactory:
    def workspace_access_repo(self, session: Session) -> UserWorkspaceAccessRepositoryProtocol:
        return DummyWorkspaceAccessRepository(session)
    
    def crud_repository(self, session: Session) ->  CrudRepositoryProtocol:
        return DummyCrudRepository(session)
        
    def user_repository(self, session: Session) -> UserRepositoryProtocol:
        return UserRepository(session)