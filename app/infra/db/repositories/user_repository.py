from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.pagination import Pagination
from app.domain.user.entity import UserEntity
from app.domain.user.user_repository_protocol import UserRepositoryProtocol
from app.infra.db.models.models import User
from app.domain.hash.entity import HashableValue

class UserRepository(UserRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            password_hash=HashableValue.from_str(model.password_hash),
            password_salt=HashableValue.from_str(model.password_salt),
            mfa_enabled=model.mfa_enabled,
            mfa_secret=HashableValue.from_str(model.mfa_secret) if model.mfa_secret else None,
            failed_login_attempts=model.failed_login_attempts,
            locked_until=model.locked_until,
            is_active=model.is_active,
            last_login_at=model.last_login_at,
            password_changed_at=model.password_changed_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: UserEntity) -> User:
        return User(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash.to_str(),
            password_salt=entity.password_salt.to_str(),
            mfa_enabled=entity.mfa_enabled,
            mfa_secret=entity.mfa_secret.to_str() if entity.mfa_secret else None,
            failed_login_attempts=entity.failed_login_attempts,
            locked_until=entity.locked_until,
            is_active=entity.is_active,
            last_login_at=entity.last_login_at,
            password_changed_at=entity.password_changed_at
        )

    def save(self, *, entity: UserEntity) -> UserEntity:
        model = self._to_model(entity)
        if model.id is None:
            self.session.add(model)
            self.session.flush()
        else:
            self.session.merge(model)
            self.session.flush()
        return self._to_entity(model)

    def delete(self, *, id: int) -> UserEntity | None:
        model = self.session.get(User, id)
        if model:
            entity = self._to_entity(model)
            self.session.delete(model)
            self.session.flush()
            return entity
        return None

    def list(self, *, pagination: Pagination | None = None) -> list[UserEntity]:
        stmt = select(User)
        if pagination:
            stmt = stmt.offset(pagination.offset).limit(pagination.limit)
        models = self.session.scalars(stmt).all()
        return [self._to_entity(m) for m in models]

    def get(self, *, id: int) -> UserEntity | None:
        model = self.session.get(User, id)
        if model:
            return self._to_entity(model)
        return None

    def get_by_email(self, *, email: str) -> UserEntity | None:
        stmt = select(User).where(User.email == email)
        model = self.session.scalars(stmt).first()
        if model:
            return self._to_entity(model)
        return None
