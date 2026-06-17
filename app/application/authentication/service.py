from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.commands import UserLoginCommand, UserRegistrationCommand
from app.application.authentication.exceptions import EmailIsExist, InvalidOrExpiredToken, InvalidPasswordOrEmail
from app.application.authentication.responses import ResolvedUserResponse
from app.domain.hash.entity import HashableValue
from app.domain.hash.hash_repository_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.domain.user.entity import UserEntity


class AuthenticationService(AuthenticationProtocol):
    """
    СЮДИ ТРЕБА ПРИКРУТИТИ JWT ТОКЕН, БО ЗАРАЗ НЕМАЄ НІЯКОГО ХЕШУВАНЯ ТОКЕНУ
    ТА І ВЗАГАЛІ ЩЕ ТРЕБА REFRESH_TOKEN
    """

    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        hash_service: HashProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._hash_service= hash_service

    
    def resolve_user(self, token: str) -> ResolvedUserResponse:
        self.verify_token(token)

        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get(id=int(token))
            
            if exist_user is None or exist_user.id is None:
                raise InvalidOrExpiredToken()
        
        return ResolvedUserResponse(
            id=exist_user.id,
            access_token=str(exist_user.id),
            token_type="bearer",
        )
        
    def verify_token(self, token: str) -> str: 
        if not token.isnumeric():
            raise Exception()
        return token
    
    def login(self, command: UserLoginCommand) -> ResolvedUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(email=command.email)
            
            if exist_user is None or exist_user.id is None:
                raise InvalidPasswordOrEmail()
            
            is_password_correct = self._hash_service.compare_hash(
                raw_value=HashableValue.from_str(command.password),
                hash=exist_user.password_hash
            )
            
            if not is_password_correct:
                raise InvalidPasswordOrEmail()
            
        return ResolvedUserResponse(
            id=exist_user.id,
            access_token=str(exist_user.id),
            token_type="bearer"
        )
    
    def register(self, command: UserRegistrationCommand) -> ResolvedUserResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(email=command.email)
            
            if exist_user is not None:
                raise EmailIsExist()
            
            password = self._hash_service.hash_value(
                HashableValue.from_str(command.password)
            )
            
            entity = UserEntity(
                name=command.surname,
                email=command.email,
                password_hash=password
            )
            
            new_user = uow.user_repo.save(
                entity=entity
            )
        
        login_user = self.login(UserLoginCommand(
            email=new_user.email,
            password=command.password,
        ))
                    
        return login_user