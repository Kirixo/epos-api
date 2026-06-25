from app.application.base import BaseResponse

class UserResponse(BaseResponse):
    id: int
    email: str
