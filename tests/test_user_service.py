import pytest
from datetime import UTC, datetime
from app.application.users.commands import UserRegistrationCommand, UserUpdateCommand
from app.application.users.exceptions import EmailAlreadyExists, InvalidOldPassword, UserNotFound
from app.application.users.service import UserService
from app.infra.services.hashing import ServerHashProvider
from app.infra.db.guow import GeneralUnitOfWorkFactory
from tests.conftest import TestingSessionFactory

@pytest.fixture
def user_service() -> UserService:
    uow_factory = GeneralUnitOfWorkFactory(TestingSessionFactory)
    hash_service = ServerHashProvider()
    return UserService(uow_factory, hash_service)

def test_register_user_success(user_service: UserService) -> None:
    cmd = UserRegistrationCommand(email="service_test@example.com", password="password123")
    resp = user_service.register(cmd)
    
    assert resp.id is not None
    assert resp.email == "service_test@example.com"
    
    # Retrieve user to verify
    profile = user_service.get_by_id(resp.id)
    assert profile.email == "service_test@example.com"

def test_register_user_duplicate_email(user_service: UserService) -> None:
    cmd = UserRegistrationCommand(email="duplicate@example.com", password="password123")
    user_service.register(cmd)
    
    with pytest.raises(EmailAlreadyExists):
        user_service.register(cmd)

def test_get_user_not_found(user_service: UserService) -> None:
    with pytest.raises(UserNotFound):
        user_service.get_by_id(9999)

def test_update_user_email_success(user_service: UserService) -> None:
    reg_cmd = UserRegistrationCommand(email="update_email@example.com", password="password123")
    user = user_service.register(reg_cmd)
    
    update_cmd = UserUpdateCommand(email="new_email@example.com")
    updated = user_service.update(user.id, update_cmd)
    
    assert updated.email == "new_email@example.com"
    
    profile = user_service.get_by_id(user.id)
    assert profile.email == "new_email@example.com"

def test_update_user_email_duplicate(user_service: UserService) -> None:
    user1 = user_service.register(UserRegistrationCommand(email="user1@example.com", password="password123"))
    user2 = user_service.register(UserRegistrationCommand(email="user2@example.com", password="password123"))
    
    update_cmd = UserUpdateCommand(email="user2@example.com")
    with pytest.raises(EmailAlreadyExists):
        user_service.update(user1.id, update_cmd)

def test_update_user_password_success(user_service: UserService) -> None:
    user = user_service.register(UserRegistrationCommand(email="update_pwd@example.com", password="password123"))
    
    update_cmd = UserUpdateCommand(password="new_password123", old_password="password123")
    updated = user_service.update(user.id, update_cmd)
    
    assert updated.id == user.id

def test_update_user_password_invalid_old(user_service: UserService) -> None:
    user = user_service.register(UserRegistrationCommand(email="update_pwd_fail@example.com", password="password123"))
    
    update_cmd = UserUpdateCommand(password="new_password123", old_password="wrongpassword")
    with pytest.raises(InvalidOldPassword):
        user_service.update(user.id, update_cmd)

def test_update_user_password_missing_old(user_service: UserService) -> None:
    user = user_service.register(UserRegistrationCommand(email="update_pwd_missing@example.com", password="password123"))
    
    update_cmd = UserUpdateCommand(password="new_password123")
    with pytest.raises(InvalidOldPassword):
        user_service.update(user.id, update_cmd)

def test_delete_user_success(user_service: UserService) -> None:
    user = user_service.register(UserRegistrationCommand(email="delete_me@example.com", password="password123"))
    
    user_service.delete(user.id)
    
    with pytest.raises(UserNotFound):
        user_service.get_by_id(user.id)

def test_delete_user_not_found(user_service: UserService) -> None:
    with pytest.raises(UserNotFound):
        user_service.delete(9999)
