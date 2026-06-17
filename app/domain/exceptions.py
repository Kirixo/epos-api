from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class GeneralException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 500):
        super().__init__(message_key, context, code)
            
