from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from os import name

from app.domain.hash.entity import HashableValue


@dataclass
class UserEntity:
    email: str
    password_hash: HashableValue
    password_salt: HashableValue
    id: int | None = None
    mfa_enabled: bool = False
    mfa_secret: HashableValue | None = None
    failed_login_attempts: int = 0
    locked_until: datetime | None = None
    is_active: bool = True
    last_login_at: datetime | None = None
    password_changed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def update(self, *,
            email: str | None = None,
            is_active: bool | None = None,
    ) -> None:
        if email is not None:
            self.email = email
        if is_active is not None:
            self.is_active = is_active
        
        self.updated_at = datetime.now(UTC)