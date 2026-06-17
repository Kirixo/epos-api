from typing import Any, Dict


class BaseInfraException(Exception):
    def __init__(self, msg: str | None = None, context: Dict[str, Any] | None = None):
        self.msg = msg
        self.context = context
        super().__init__(self.msg)
