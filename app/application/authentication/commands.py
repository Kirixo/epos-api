from app.application.base import FlexibleCommand


class UserLoginCommand(FlexibleCommand):
    email: str
    password: str


class TokenRefreshCommand(FlexibleCommand):
    refresh_token: str
