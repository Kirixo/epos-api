from datetime import UTC, datetime
from app.application.users.commands import UserRegistrationCommand, UserUpdateCommand
from app.application.users.exceptions import EmailAlreadyExists, InvalidOldPassword, UserNotFound
from app.application.users.responses import UserResponse
from app.application.users.user_protocol import UserServiceProtocol
from app.domain.hash.entity import HashableValue
from app.domain.hash.hash_repository_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.domain.user.entity import UserEntity

class UserService(UserServiceProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        hash_service: HashProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._hash_service = hash_service

    def register(self, command: UserRegistrationCommand) -> UserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(email=command.email)
            if exist_user is not None:
                raise EmailAlreadyExists()
            
            hashed_pwd = self._hash_service.hash_value(
                HashableValue.from_str(command.password)
            )
            
            # Use random salt or fallback to hash for salt representation
            salt = self._hash_service.random_hash()
            
            entity = UserEntity(
                email=command.email,
                password_hash=hashed_pwd,
                password_salt=salt
            )
            
            new_user = uow.user_repo.save(entity=entity)
            
            if new_user.id is None:
                raise Exception("Failed to save user")
            
            return UserResponse(
                id=new_user.id,
                email=new_user.email
            )

    def update(self, user_id: int, command: UserUpdateCommand) -> UserResponse:
        with self._uow_factory.create() as uow:
            user = uow.user_repo.get(id=user_id)
            if user is None:
                raise UserNotFound()

            # If email is updating, verify uniqueness
            if command.email and command.email != user.email:
                existing_email_user = uow.user_repo.get_by_email(email=command.email)
                if existing_email_user is not None:
                    raise EmailAlreadyExists()
                user.email = command.email

            # If password is updating, verify old password
            if command.password:
                if not command.old_password:
                    raise InvalidOldPassword()
                
                is_correct = self._hash_service.compare_hash(
                    raw_value=HashableValue.from_str(command.old_password),
                    hash=user.password_hash
                )
                if not is_correct:
                    raise InvalidOldPassword()
                
                hashed_pwd = self._hash_service.hash_value(
                    HashableValue.from_str(command.password)
                )
                user.password_hash = hashed_pwd
                user.password_changed_at = datetime.now(UTC)

            updated_user = uow.user_repo.save(entity=user)
            
            if updated_user.id is None:
                raise Exception("Failed to update user")
            
            return UserResponse(
                id=updated_user.id,
                email=updated_user.email
            )

    def delete(self, user_id: int) -> None:
        with self._uow_factory.create() as uow:
            user = uow.user_repo.get(id=user_id)
            if user is None:
                raise UserNotFound()
            
            uow.user_repo.delete(id=user_id)

    def get_by_id(self, user_id: int) -> UserResponse:
        with self._uow_factory.create() as uow:
            user = uow.user_repo.get(id=user_id)
            if user is None:
                raise UserNotFound()
            
            if user.id is None:
                raise Exception("Invalid user ID")
                
            return UserResponse(
                id=user.id,
                email=user.email
            )
