# ФАБРИКА

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.responses import CurrentUserResponse
from app.application.authentication.service import AuthenticationService
from app.application.users.user_protocol import UserServiceProtocol
from app.application.users.service import UserService
from app.domain.hash.hash_repository_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.db.guow import GeneralUnitOfWorkFactory
from app.infra.db.session import SessionFactory
from app.infra.services.hashing import ServerHashProvider


def get_hash_provider() -> HashProtocol:
    return ServerHashProvider()


def get_uow_factory() -> UnitOfWorkFactoryProtocol:
    return GeneralUnitOfWorkFactory(SessionFactory)


def get_user_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    hash_service: HashProtocol = Depends(get_hash_provider),
) -> UserServiceProtocol:
    return UserService(uow_factory, hash_service)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")


def get_authentication_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    hash_service: HashProtocol = Depends(get_hash_provider),
) -> AuthenticationProtocol:
    return AuthenticationService(
        uow_factory,
        hash_service,
    )


def resolve_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthenticationProtocol = Depends(get_authentication_service),
) -> CurrentUserResponse:
    return auth_service.resolve_user(token)
