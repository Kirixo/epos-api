from __future__ import annotations

from typing import Protocol

from app.domain.user.revoked_token_entity import RevokedTokenEntity


class RevokedTokenRepositoryProtocol(Protocol):
    def save(self, *, entity: RevokedTokenEntity) -> RevokedTokenEntity: ...
    def is_revoked(self, *, token_signature: str) -> bool: ...
