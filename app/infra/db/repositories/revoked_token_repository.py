from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.user.revoked_token_entity import RevokedTokenEntity
from app.domain.user.revoked_token_repository_protocol import RevokedTokenRepositoryProtocol
from app.infra.db.models.models import RevokedToken


class RevokedTokenRepository(RevokedTokenRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_entity(self, model: RevokedToken) -> RevokedTokenEntity:
        return RevokedTokenEntity(
            id=model.id,
            user_id=model.user_id,
            token_signature=model.token_signature,
            expires_at=model.expires_at,
        )

    def _to_model(self, entity: RevokedTokenEntity) -> RevokedToken:
        return RevokedToken(
            id=entity.id,
            user_id=entity.user_id,
            token_signature=entity.token_signature,
            expires_at=entity.expires_at,
        )

    def save(self, *, entity: RevokedTokenEntity) -> RevokedTokenEntity:
        model = self._to_model(entity)
        self.session.add(model)
        self.session.flush()
        return self._to_entity(model)

    def is_revoked(self, *, token_signature: str) -> bool:
        stmt = select(RevokedToken.id).where(RevokedToken.token_signature == token_signature)
        return self.session.scalar(stmt) is not None
