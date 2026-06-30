from datetime import datetime

from app.application.base import BaseResponse

class UserResponse(BaseResponse):
    id: int
    email: str
    created_at: datetime | None
    updated_at: datetime | None
