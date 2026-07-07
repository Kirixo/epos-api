# ФАБРИКА

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.responses import CurrentUserResponse
from app.application.authentication.service import AuthenticationService
from app.application.sync.service import WorkspaceSyncService
from app.application.users.user_protocol import UserServiceProtocol
from app.application.users.service import UserService
from app.domain.hash.hash_repository_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.core.config import settings
from app.infra.db.guow import GeneralUnitOfWorkFactory
from app.infra.db.session import SessionFactory
from app.infra.services.hashing import ServerHashProvider
from app.infra.sync.mongo_repository import MongoWorkspaceSyncRepository
from typing import Any
from pymongo import MongoClient


_mongo_client: MongoClient[Any] | None = None


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


def get_sync_repository() -> MongoWorkspaceSyncRepository:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=2000)

    return MongoWorkspaceSyncRepository(_mongo_client, settings.mongo_db)


def get_sync_service(
    repository: MongoWorkspaceSyncRepository = Depends(get_sync_repository),
) -> WorkspaceSyncService:
    return WorkspaceSyncService(repository)
