from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.commands import UserLoginCommand
from app.application.authentication.responses import ResolvedUserResponse
from app.application.base import JsonDict
from app.di.dependencies import get_authentication_service

router = APIRouter()

@router.post("/token", response_model=ResolvedUserResponse, tags=["auth"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthenticationProtocol = Depends(get_authentication_service)
) -> JsonDict:
    resolved_user = auth_service.login(
        UserLoginCommand(
            email=form_data.username, 
            password=form_data.password
        )
    )
    return resolved_user.model_dump()
