from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.domain.hash.entity import HashableValue

@dataclass
class AuditLogEntity:
    user_id: int
    action: str
    details: dict[str, Any]
    ip_hash: HashableValue
    ip_salt: HashableValue
    id: int | None = None
    created_at: datetime | None = None
