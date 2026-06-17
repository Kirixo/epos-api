from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from os import name

from app.domain.hash.entity import HashableValue


@dataclass
class UserEntity:
    name: str
    email:str
    password_hash: HashableValue
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def update(self, *,
            name: str | None = None,
            email: str | None = None,
    ) -> None:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        
        self.updated_at = datetime.now(UTC)