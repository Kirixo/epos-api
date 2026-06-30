from typing import Protocol

from app.application.authentication.commands import TokenRefreshCommand, UserLoginCommand
from app.application.authentication.responses import CurrentUserResponse, TokenPairResponse


class AuthenticationProtocol(Protocol):

    def resolve_user(self, token: str) -> CurrentUserResponse: ...
    def login(self, command: UserLoginCommand) -> TokenPairResponse: ...
    def refresh(self, command: TokenRefreshCommand) -> TokenPairResponse: ...
