from app.application.base import FlexibleCommand


class UserLoginCommand(FlexibleCommand):
    email: str
    password: str
    