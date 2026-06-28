from __future__ import annotations

from datetime import UTC, datetime

from app.application.authentication.authentication_protocol import AuthenticationProtocol
from app.application.authentication.commands import TokenRefreshCommand, UserLoginCommand
from app.application.authentication.exceptions import (
    InvalidOrExpiredToken,
    InvalidPasswordOrEmail,
    RefreshTokenAlreadyUsed,
)
from app.application.authentication.jwt_constants import ACCESS_TOKEN_EXPIRES, REFRESH_TOKEN_EXPIRES
from app.application.authentication.responses import CurrentUserResponse, TokenPairResponse
from app.application.authentication.token_utils import create_token, decode_jwt
from app.domain.hash.entity import HashableValue
from app.domain.hash.hash_repository_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.domain.user.revoked_token_entity import RevokedTokenEntity


class AuthenticationService(AuthenticationProtocol):
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        hash_service: HashProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._hash_service = hash_service

    def resolve_user(self, token: str) -> CurrentUserResponse:
        payload = self._decode_token(token, expected_type="access")
        user_id = int(payload["sub"])

        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get(id=user_id)
            if exist_user is None or exist_user.id is None:
                raise InvalidOrExpiredToken()

        return CurrentUserResponse(
            id=exist_user.id,
            email=exist_user.email,
        )

    def login(self, command: UserLoginCommand) -> TokenPairResponse:
        with self._uow_factory.create() as uow:
            exist_user = uow.user_repo.get_by_email(email=command.email)
            if exist_user is None or exist_user.id is None:
                raise InvalidPasswordOrEmail()

            is_password_correct = self._hash_service.compare_hash(
                raw_value=HashableValue.from_str(command.password),
                hash=exist_user.password_hash,
            )
            if not is_password_correct:
                raise InvalidPasswordOrEmail()

        return self._issue_token_pair(user_id=exist_user.id)

    def refresh(self, command: TokenRefreshCommand) -> TokenPairResponse:
        payload = self._decode_token(command.refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])
        token_signature = str(payload["jti"])
        expires_at = datetime.fromtimestamp(float(payload["exp"]), UTC)

        with self._uow_factory.create() as uow:
            if uow.revoked_token_repo.is_revoked(token_signature=token_signature):
                raise RefreshTokenAlreadyUsed()

            exist_user = uow.user_repo.get(id=user_id)
            if exist_user is None or exist_user.id is None:
                raise InvalidOrExpiredToken()

            uow.revoked_token_repo.save(
                entity=RevokedTokenEntity(
                    user_id=user_id,
                    token_signature=token_signature,
                    expires_at=expires_at,
                )
            )

        return self._issue_token_pair(user_id=user_id)

    def _issue_token_pair(self, *, user_id: int) -> TokenPairResponse:
        return TokenPairResponse(
            id=user_id,
            access_token=create_token(
                user_id=user_id,
                token_type="access",
                expires_delta=ACCESS_TOKEN_EXPIRES,
            ),
            refresh_token=create_token(
                user_id=user_id,
                token_type="refresh",
                expires_delta=REFRESH_TOKEN_EXPIRES,
            ),
            token_type="bearer",
        )

    def _decode_token(self, token: str, *, expected_type: str) -> dict[str, str | int]:
        try:
            decoded = decode_jwt(token).payload
        except ValueError as exc:
            raise InvalidOrExpiredToken() from exc

        if decoded.get("typ") != expected_type:
            raise InvalidOrExpiredToken()

        sub = decoded.get("sub")
        if not isinstance(sub, str) or not sub.isdigit():
            raise InvalidOrExpiredToken()

        jti = decoded.get("jti")
        if not isinstance(jti, str) or not jti:
            raise InvalidOrExpiredToken()

        exp = decoded.get("exp")
        if not isinstance(exp, int):
            raise InvalidOrExpiredToken()

        return {
            "sub": sub,
            "jti": jti,
            "exp": exp,
            "typ": expected_type,
        }
