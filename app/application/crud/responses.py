from __future__ import annotations

from datetime import datetime
from typing import Any

from app.application.base import BaseResponse


class CrudValue(BaseResponse):
    id: int
    item_name: str
    item_value: str
    updated_at: datetime | None = None

class GetCrudResponse(BaseResponse):
    value: CrudValue
    
class CreateCrudResponse(BaseResponse):
    value: CrudValue
    
class ListCrudResponse(BaseResponse):
    values: list[CrudValue]
    
class DeleteCrudResponse(BaseResponse):
    id: int
    
class UpdateCrudResponse(BaseResponse):
    value: CrudValue