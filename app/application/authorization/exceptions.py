from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class AuthorizationException(BaseBoundaryException):
    def __init__(self, message_key: str = "authorization.denied", context: Dict[str, Any]={}, code: int = 403):
        super().__init__(message_key, context, code)
