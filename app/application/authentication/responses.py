from app.application.base import BaseResponse

class ResolvedUserResponse(BaseResponse):
    id: int
    access_token: str
    token_type: str
