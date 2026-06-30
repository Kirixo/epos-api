from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form

from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.commands import TokenRefreshCommand, UserLoginCommand
from app.application.authentication.responses import TokenPairResponse
from app.application.base import JsonDict
from app.di.dependencies import get_authentication_service

router = APIRouter()


class EmailPasswordForm:
    def __init__(
        self,
        email: Annotated[str, Form(...)],
        password: Annotated[str, Form(...)],
    ) -> None:
        self.email = email
        self.password = password


@router.post("/token", response_model=TokenPairResponse, tags=["auth"])
def login(
    form_data: Annotated[EmailPasswordForm, Depends()],
    auth_service: AuthenticationProtocol = Depends(get_authentication_service),
) -> JsonDict:
    token_pair = auth_service.login(
        UserLoginCommand(
            email=form_data.email,
            password=form_data.password,
        )
    )
    return token_pair.model_dump()


@router.post("/refresh", response_model=TokenPairResponse, tags=["auth"])
def refresh(
    refresh_token: Annotated[str, Body(embed=True)],
    auth_service: AuthenticationProtocol = Depends(get_authentication_service),
) -> JsonDict:
    token_pair = auth_service.refresh(
        TokenRefreshCommand(refresh_token=refresh_token),
    )
    return token_pair.model_dump()
