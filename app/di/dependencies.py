# ФАБРИКА

from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncIterator

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.responses import ResolvedUserResponse
from app.application.authentication.service import AuthenticationService
from app.application.authorization.service import AuthorizationService
from app.application.contracts.value_codec import ValueCodecProtocol
from app.application.crud.service import CrudService
from app.domain.hash.hash_repository_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.db.guow import GeneralUnitOfWorkFactory
from app.infra.db.session import SessionFactory
from app.infra.services.hashing import ServerHashProvider

# ======================================================
# Інфра сервіси
# ======================================================

def get_hash_provider() -> HashProtocol:
    return ServerHashProvider()

def get_uow_factory() -> UnitOfWorkFactoryProtocol:
    return GeneralUnitOfWorkFactory(SessionFactory)


# ======================================================
# Аплікації сервіси
# ======================================================

def get_authorization_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
) -> AuthorizationService:
    return AuthorizationService(uow_factory)

def get_crud_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    authorization_service: AuthorizationService = Depends(get_authorization_service),
) -> CrudService:
    return CrudService(uow_factory, authorization_service)


# ======================================================
# Індефікація юзера
# ======================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# АААААААААААААААААААА АНТИПАТЕРНИ
@lru_cache
def user_resolver(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    hash_service: HashProtocol = Depends(get_hash_provider)
) -> AuthenticationProtocol:
    return AuthenticationService(
        uow_factory,
        hash_service
    )


def resolve_user(
    token: str = Depends(oauth2_scheme),
    user_resolver: AuthenticationProtocol = Depends(user_resolver)
) -> ResolvedUserResponse:
    return user_resolver.resolve_user(token)
