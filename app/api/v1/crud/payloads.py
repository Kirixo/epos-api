from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from app.api.v1.transport import TransportPayload

class CreateItemPayload(TransportPayload):
    item_name: str
    item_value: str
    
class DeleteItemPayload(TransportPayload):
    id: int
    
class UpdateItemPayload(TransportPayload):
    item_name: str | None
    item_value: str | None
    occurred_at: datetime | None = None
