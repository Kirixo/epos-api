from typing import Annotated
from fastapi import APIRouter, Body, Depends, Request, Response, status

from app.api.v1.users.payloads import UserRegistrationPayload, UserUpdatePayload, UserResponsePayload
from app.application.users.user_protocol import UserServiceProtocol
from app.application.users.commands import UserRegistrationCommand, UserUpdateCommand
from app.application.authentication.responses import ResolvedUserResponse
from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.commands import UserLoginCommand
from app.application.base import JsonDict
from app.di.dependencies import get_user_service, resolve_user, get_authentication_service

router = APIRouter()

@router.post("/register", response_model=ResolvedUserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def register(
    body: Annotated[UserRegistrationPayload, Body()],
    user_service: UserServiceProtocol = Depends(get_user_service),
    auth_service: AuthenticationProtocol = Depends(get_authentication_service),
) -> JsonDict:
    # 1. Register the user
    user_resp = user_service.register(
        UserRegistrationCommand(
            email=body.email,
            password=body.password
        )
    )
    # 2. Login the registered user to return the token
    login_user = auth_service.login(
        UserLoginCommand(
            email=body.email,
            password=body.password
        )
    )
    return login_user.model_dump()

@router.get("/me", response_model=UserResponsePayload, tags=["users"])
def get_me(
    current_user: Annotated[ResolvedUserResponse, Depends(resolve_user)],
    user_service: UserServiceProtocol = Depends(get_user_service),
) -> JsonDict:
    user_resp = user_service.get_by_id(current_user.id)
    return user_resp.model_dump()

@router.patch("/me", response_model=UserResponsePayload, tags=["users"])
def update_me(
    body: Annotated[UserUpdatePayload, Body()],
    current_user: Annotated[ResolvedUserResponse, Depends(resolve_user)],
    user_service: UserServiceProtocol = Depends(get_user_service),
) -> JsonDict:
    user_resp = user_service.update(
        user_id=current_user.id,
        command=UserUpdateCommand(
            email=body.email,
            password=body.password,
            old_password=body.old_password
        )
    )
    return user_resp.model_dump()

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_me(
    current_user: Annotated[ResolvedUserResponse, Depends(resolve_user)],
    user_service: UserServiceProtocol = Depends(get_user_service),
) -> Response:
    user_service.delete(current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
