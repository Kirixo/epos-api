from datetime import UTC, datetime
from unittest.mock import MagicMock

from app.domain.hash.entity import HashableValue
from app.domain.user.entity import UserEntity
from app.infra.db.models.models import User
from app.infra.db.repositories.user_repository import UserRepository


def test_to_model() -> None:
    repo = UserRepository(session=MagicMock())
    now = datetime.now(UTC)
    entity = UserEntity(
        id=1,
        email="test@example.com",
        password_hash=HashableValue.from_str("hash"),
        password_salt=HashableValue.from_str("salt"),
        mfa_enabled=True,
        mfa_secret=HashableValue.from_str("secret"),
        failed_login_attempts=2,
        locked_until=now,
        is_active=True,
        last_login_at=now,
        password_changed_at=now,
        created_at=now,
        updated_at=now
    )
    
    model = repo._to_model(entity)
    
    assert model.id == 1
    assert model.email == "test@example.com"
    assert model.password_hash == "hash"
    assert model.password_salt == "salt"
    assert model.mfa_enabled is True
    assert model.mfa_secret == "secret"
    assert model.failed_login_attempts == 2
    assert model.locked_until == now
    assert model.is_active is True
    assert model.last_login_at == now
    assert model.password_changed_at == now


def test_to_entity() -> None:
    repo = UserRepository(session=MagicMock())
    now = datetime.now(UTC)
    model = User(
        id=1,
        email="test@example.com",
        password_hash="hash",
        password_salt="salt",
        mfa_enabled=True,
        mfa_secret="secret",
        failed_login_attempts=2,
        locked_until=now,
        is_active=True,
        last_login_at=now,
        password_changed_at=now,
        created_at=now,
        updated_at=now
    )
    
    entity = repo._to_entity(model)
    
    assert entity.id == 1
    assert entity.email == "test@example.com"
    assert entity.password_hash.to_str() == "hash"
    assert entity.password_salt.to_str() == "salt"
    assert entity.mfa_enabled is True
    assert entity.mfa_secret and entity.mfa_secret.to_str() == "secret"
    assert entity.failed_login_attempts == 2
    assert entity.locked_until == now
    assert entity.is_active is True
    assert entity.last_login_at == now
    assert entity.password_changed_at == now
    assert entity.created_at == now
    assert entity.updated_at == now


def test_save_new() -> None:
    session_mock = MagicMock()
    repo = UserRepository(session=session_mock)
    entity = UserEntity(email="test@example.com", password_hash=HashableValue.from_str("h"), password_salt=HashableValue.from_str("s"))
    
    result = repo.save(entity=entity)
    
    session_mock.add.assert_called_once()
    session_mock.flush.assert_called_once()
    assert result.email == "test@example.com"


def test_save_existing() -> None:
    session_mock = MagicMock()
    repo = UserRepository(session=session_mock)
    entity = UserEntity(id=1, email="test@example.com", password_hash=HashableValue.from_str("h"), password_salt=HashableValue.from_str("s"))
    
    result = repo.save(entity=entity)
    
    session_mock.merge.assert_called_once()
    session_mock.flush.assert_called_once()
    assert result.id == 1


def test_delete_existing() -> None:
    session_mock = MagicMock()
    now = datetime.now(UTC)
    model = User(id=1, email="test@example.com", password_hash="h", password_salt="s", mfa_enabled=False, failed_login_attempts=0, is_active=True, created_at=now, updated_at=now)
    session_mock.get.return_value = model
    
    repo = UserRepository(session=session_mock)
    result = repo.delete(id=1)
    
    session_mock.delete.assert_called_once_with(model)
    session_mock.flush.assert_called_once()
    assert result is not None
    assert result.id == 1


def test_delete_missing() -> None:
    session_mock = MagicMock()
    session_mock.get.return_value = None
    
    repo = UserRepository(session=session_mock)
    result = repo.delete(id=99)
    
    session_mock.delete.assert_not_called()
    assert result is None


def test_list() -> None:
    session_mock = MagicMock()
    now = datetime.now(UTC)
    model = User(id=1, email="test@example.com", password_hash="h", password_salt="s", mfa_enabled=False, failed_login_attempts=0, is_active=True, created_at=now, updated_at=now)
    session_mock.scalars.return_value.all.return_value = [model]
    
    repo = UserRepository(session=session_mock)
    results = repo.list()
    
    assert len(results) == 1
    assert results[0].id == 1


def test_get_existing() -> None:
    session_mock = MagicMock()
    now = datetime.now(UTC)
    model = User(id=1, email="test@example.com", password_hash="h", password_salt="s", mfa_enabled=False, failed_login_attempts=0, is_active=True, created_at=now, updated_at=now)
    session_mock.get.return_value = model
    
    repo = UserRepository(session=session_mock)
    result = repo.get(id=1)
    
    assert result is not None
    assert result.id == 1


def test_get_missing() -> None:
    session_mock = MagicMock()
    session_mock.get.return_value = None
    
    repo = UserRepository(session=session_mock)
    result = repo.get(id=99)
    
    assert result is None


def test_get_by_email_existing() -> None:
    session_mock = MagicMock()
    now = datetime.now(UTC)
    model = User(id=1, email="test@example.com", password_hash="h", password_salt="s", mfa_enabled=False, failed_login_attempts=0, is_active=True, created_at=now, updated_at=now)
    session_mock.scalars.return_value.first.return_value = model
    
    repo = UserRepository(session=session_mock)
    result = repo.get_by_email(email="test@example.com")
    
    assert result is not None
    assert result.email == "test@example.com"


def test_get_by_email_missing() -> None:
    session_mock = MagicMock()
    session_mock.scalars.return_value.first.return_value = None
    
    repo = UserRepository(session=session_mock)
    result = repo.get_by_email(email="missing@example.com")
    
    assert result is None
