from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.authentication.payloads import UserRegistrationSchemaPayload
from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.commands import UserLoginCommand, UserRegistrationCommand
from app.application.base import JsonDict
from app.di.dependencies import user_resolver


router = APIRouter()

@router.post("/token", tags=["authentication"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authentication_service: AuthenticationProtocol = Depends(user_resolver)
) -> JsonDict:
    resolved_user = authentication_service.login(
        UserLoginCommand(
            email=form_data.username, 
            password=form_data.password
        )
    )
    return resolved_user.model_dump()

@router.post("/register", tags=["authentication"])
def register(
    body: Annotated[UserRegistrationSchemaPayload, Body()],
    authentication_service: AuthenticationProtocol = Depends(user_resolver),
) -> JsonDict:
    resolved_user = authentication_service.register(
        UserRegistrationCommand(
            email=body.email,
            password=body.password,
            name=body.name,
            surname=body.surname,
            nickname=body.nickname
        )
    )
    
    return resolved_user.model_dump()
