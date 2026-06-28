from sqlalchemy.orm import Session

from app.domain.access.user_access_repository_protocol import UserWorkspaceAccessRepositoryProtocol
from app.domain.user.user_repository_protocol import UserRepositoryProtocol
from app.domain.user.revoked_token_repository_protocol import RevokedTokenRepositoryProtocol
from app.infra.db.repositories.user_repository import UserRepository
from app.infra.db.repositories.revoked_token_repository import RevokedTokenRepository
from app.domain.access.entity import UserWorkspaceAccessEntity
from app.domain.pagination import Pagination


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

    def delete(self, *, user_id: int, app_id: int) -> UserWorkspaceAccessEntity:
        raise NotImplementedError

    def list_by_workspace_id(
        self,
        *,
        workspace_id: int,
        pagination: Pagination | None = None,
    ) -> list[UserWorkspaceAccessEntity]:
        raise NotImplementedError


class GeneralRepositoriesFactory:
    def workspace_access_repo(self, session: Session) -> UserWorkspaceAccessRepositoryProtocol:
        return DummyWorkspaceAccessRepository(session)

    def user_repository(self, session: Session) -> UserRepositoryProtocol:
        return UserRepository(session)

    def revoked_token_repository(self, session: Session) -> RevokedTokenRepositoryProtocol:
        return RevokedTokenRepository(session)
