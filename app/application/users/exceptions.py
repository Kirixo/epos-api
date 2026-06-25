from typing import Any, Dict
from app.core.exception import BaseBoundaryException

class UserException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int=500):
        super().__init__(message_key, context, code)

class EmailAlreadyExists(UserException):
    def __init__(self) -> None:
        super().__init__(message_key="email_exists", code=400)

class InvalidOldPassword(UserException):
    def __init__(self) -> None:
        super().__init__(message_key="invalid_old_password", code=400)

class UserNotFound(UserException):
    def __init__(self) -> None:
        super().__init__(message_key="user_not_found", code=404)
