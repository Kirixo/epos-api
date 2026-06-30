from app.application.base import FlexibleCommand

class UserRegistrationCommand(FlexibleCommand):
    email: str
    password: str

class UserUpdateCommand(FlexibleCommand):
    email: str | None = None
    password: str | None = None
    old_password: str | None = None
