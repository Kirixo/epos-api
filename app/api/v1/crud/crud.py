from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, Query, status

from app.api.v1.crud.payloads import *
from app.api.v1.payloads import WorkSpaceScopedQueryPayload
from app.api.v1.transport import PaginationQueryPayload
from app.application.authentication.responses import ResolvedUserResponse
from app.application.crud.mappers import CrudCommandMapper
from app.application.crud.service import CrudService
from app.core.utils.general_mapper import GeneralMapper
from app.di.dependencies import get_crud_service, resolve_user

router = APIRouter()


@router.get("/")
def get_list(
    pagination_queries: Annotated[PaginationQueryPayload, Query()],
    work_space_scoped_queries: Annotated[WorkSpaceScopedQueryPayload, Query()],
    
    service: CrudService = Depends(get_crud_service),
    user: ResolvedUserResponse = Depends(resolve_user),
) -> str:
    command = CrudCommandMapper.list_from_transport(
        GeneralMapper.to_dict(pagination_queries, work_space_scoped_queries, user_id=user.id)
    )
    response = service.get_list(command)
    return response.model_dump_json()

@router.get("/{id}")
def get(
    id: int,
    work_space_scoped_queries: Annotated[WorkSpaceScopedQueryPayload, Query()],
    
    service: CrudService = Depends(get_crud_service),
    user: ResolvedUserResponse = Depends(resolve_user),
) -> str:
    command = CrudCommandMapper.get_from_transport(
        GeneralMapper.to_dict(work_space_scoped_queries, item_id=id, user_id=user.id)
    )
    response = service.get(command)
    return response.model_dump_json()

@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
def update(
    id: int,
    payload: Annotated[UpdateItemPayload, Body()],
    work_space_scoped_queries: Annotated[WorkSpaceScopedQueryPayload, Query()],
    
    service: CrudService = Depends(get_crud_service),
    user: ResolvedUserResponse = Depends(resolve_user),
) -> str:
    command = CrudCommandMapper.update_from_transport(
        GeneralMapper.to_dict(payload, work_space_scoped_queries, item_id=id, user_id=user.id)
    )
    response = service.update(command)
    return response.model_dump_json()

@router.delete("/{id}", status_code=status.HTTP_201_CREATED)
def delete(
    id: int,
    work_space_scoped_queries: Annotated[WorkSpaceScopedQueryPayload, Query()],
    
    service: CrudService = Depends(get_crud_service),
    user: ResolvedUserResponse = Depends(resolve_user),
) -> str:
    command = CrudCommandMapper.delete_from_transport(
        GeneralMapper.to_dict(work_space_scoped_queries, item_id=id, user_id=user.id)
    )
    response = service.delete(command)
    return response.model_dump_json()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    payload: Annotated[CreateItemPayload, Body()],
    work_space_scoped_queries: Annotated[WorkSpaceScopedQueryPayload, Query()],
    
    service: CrudService = Depends(get_crud_service),
    user: ResolvedUserResponse = Depends(resolve_user),
) -> str:
    command = CrudCommandMapper.create_from_transport(
        GeneralMapper.to_dict(payload, work_space_scoped_queries, user_id=user.id)
    )
    response = service.create(command)
    return response.model_dump_json()

