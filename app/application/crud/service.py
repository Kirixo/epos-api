from __future__ import annotations

from app.application.authorization.service import AuthorizationService
from app.application.contracts.value_codec import ValueCodecProtocol
from app.application.crud.commands import *
from app.application.crud.exceptions import CrudNotFound
from app.application.crud.mappers import CrudResponseMapper
from app.application.crud.responses import *
from app.application.mapper import PaginationMapper
from app.domain.crud.entity import CrudEntity
from app.domain.uow import UnitOfWorkFactoryProtocol


class CrudService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        authorization_service: AuthorizationService,
    ) -> None:
        self._uow_factory = uow_factory
        self._authorization_service = authorization_service

    def create(
        self,
        command: CreateCrudCommand,
    ) -> CreateCrudResponse:
        self._authorization_service.has_user_workspace_access(
            workspace_id=command.workspace_id, 
            user_id=command.user_id
        )
        
        with self._uow_factory.create() as uow:
            entity = CrudEntity.create(
                item_name=command.item_name,
                item_value=command.item_value
            )
            
            entity = uow.crud_repo.save(entity=entity)
        
        return CreateCrudResponse(
            value=CrudResponseMapper.crud_to_value(entity=entity)
        )
            

    def get(
        self,
        command: GetCrudCommand,
    ) -> GetCrudResponse:
        self._authorization_service.has_user_workspace_access(
            workspace_id=command.workspace_id, 
            user_id=command.user_id
        )
        
        with self._uow_factory.create() as uow:
            entity=uow.crud_repo.get(id=command.item_id)
            if entity is None: 
                raise CrudNotFound(id=command.item_id)
        
        return GetCrudResponse(
            value=CrudResponseMapper.crud_to_value(entity=entity)
        ) 
        
        
    def get_list(
        self,
        command: ListCrudCommand,
    ) -> ListCrudResponse:
        self._authorization_service.has_user_workspace_access(
            workspace_id=command.workspace_id, 
            user_id=command.user_id
        )
        with self._uow_factory.create() as uow:
            entities=uow.crud_repo.list(
                pagination=PaginationMapper.pagination_from_command(command)
            )
        
        return ListCrudResponse(
            values=[CrudResponseMapper.crud_to_value(entity=it) for it in entities]
        ) 
        
        
    def update(
        self,
        command: UpdateCrudCommand,
    ) -> UpdateCrudResponse:
        self._authorization_service.has_user_workspace_access(
            workspace_id=command.workspace_id, 
            user_id=command.user_id
        )
        
        with self._uow_factory.create() as uow:
            entity=uow.crud_repo.get(id=command.item_id)
            if entity is None: 
                raise CrudNotFound(id=command.item_id)
            
            entity.update(
                item_name=command.item_name,
                item_value=command.item_value
            )
            
            entity = uow.crud_repo.save(entity=entity)
        
        return UpdateCrudResponse(
            value=CrudResponseMapper.crud_to_value(entity=entity)
        ) 
            
        
    def delete(
        self,
        command: DeleteCrudCommand,
    ) -> DeleteCrudResponse:
        self._authorization_service.has_user_workspace_access(
            workspace_id=command.workspace_id, 
            user_id=command.user_id
        )
        
        with self._uow_factory.create() as uow:
            entity=uow.crud_repo.get(id=command.item_id)
            if entity is None: 
                raise CrudNotFound(id=command.item_id)
            
            entity=uow.crud_repo.delete(id=command.item_id)
            
        return DeleteCrudResponse(
            id=entity.id
        ) 
            