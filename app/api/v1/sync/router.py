from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from app.api.v1.sync.payloads import SyncPushPayload
from app.application.authentication.responses import CurrentUserResponse
from app.application.base import JsonDict
from app.application.sync.service import WorkspaceSyncService
from app.di.dependencies import get_sync_service, resolve_user

router = APIRouter()


@router.post("/push", tags=["sync"])
def push_sync(
    body: Annotated[SyncPushPayload, Body()],
    current_user: Annotated[CurrentUserResponse, Depends(resolve_user)],
    sync_service: WorkspaceSyncService = Depends(get_sync_service),
) -> JsonDict:
    response = sync_service.push(
        user_id=current_user.id,
        workspace_id=body.workspace_id,
        payload=body.payload,
    )
    return response.model_dump()


@router.get("/pull", tags=["sync"])
def pull_sync(
    workspace_id: Annotated[str, Query(min_length=1)],
    current_user: Annotated[CurrentUserResponse, Depends(resolve_user)],
    after_cursor: Annotated[str | None, Query()] = None,
    sync_service: WorkspaceSyncService = Depends(get_sync_service),
) -> JsonDict:
    response = sync_service.pull(
        user_id=current_user.id,
        workspace_id=workspace_id,
        after_cursor=after_cursor,
    )
    return response.model_dump()
