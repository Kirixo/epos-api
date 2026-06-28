from app.application.base import BaseResponse


class TokenPairResponse(BaseResponse):
    id: int
    access_token: str
    refresh_token: str
    token_type: str


class CurrentUserResponse(BaseResponse):
    id: int
    email: str
