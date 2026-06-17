from dataclasses import dataclass

from app.application.authorization.exceptions import AuthorizationException
from app.application.exception import UserNotFound, WorkspaceNotFound
from app.domain.access.entity import UserWorkspaceAccessEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol

class AuthorizationService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
    ) -> None:
        self._uow_factory = uow_factory
    
    def _get_user_access(self, uow: UnitOfWorkProtocol, *, user_id: int, workspace_id: int) -> UserWorkspaceAccessEntity | None:
        access = uow.workspace_access_repo.get_by_user_and_workspace(user_id=user_id, workspace_id=workspace_id)
        return access

    def has_user_workspace_access(self, *, user_id: int, workspace_id: int) -> None:
        with self._uow_factory.create() as uow:
            if uow.user_repo.get(id=user_id) is None:
                raise UserNotFound()
            
            if uow.user_repo.get(id=user_id) is None:
                raise WorkspaceNotFound()
            
            access = self._get_user_access(uow, user_id = user_id, workspace_id = workspace_id)
        
        if  access is None:
            raise AuthorizationException()
