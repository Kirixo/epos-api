from dataclasses import dataclass
from datetime import datetime

@dataclass
class RevokedTokenEntity:
    user_id: int
    token_signature: str
    expires_at: datetime
    id: int | None = None
