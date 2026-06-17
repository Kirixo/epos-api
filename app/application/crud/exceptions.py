from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class CrudException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any]={}, code: int = 500):
        super().__init__(message_key, context, code)

class CrudNotFound(CrudException):
    def __init__(self, *, id: int) -> None:
        super().__init__("crud.not_found", {"id":id}, 404)
