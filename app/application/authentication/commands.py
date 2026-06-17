from app.application.base import FlexibleCommand


class UserLoginCommand(FlexibleCommand):
    email: str
    password: str
    
class UserRegistrationCommand(FlexibleCommand):
    email: str
    password: str
    name: str
    surname: str
    nickname: str
    