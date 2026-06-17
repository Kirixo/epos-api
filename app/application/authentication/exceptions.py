from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class AuthenticationException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int=500):
        super().__init__(message_key, context, code)

class InvalidOrExpiredToken(AuthenticationException):
    def __init__(self) -> None:
        super().__init__()
        
class InvalidPasswordOrEmail(AuthenticationException):
    def __init__(self) -> None:
        super().__init__()
        
class EmailIsExist(AuthenticationException):
    def __init__(self) -> None:
        super().__init__()