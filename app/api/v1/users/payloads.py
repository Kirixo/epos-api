from datetime import datetime

from pydantic import BaseModel, Field

class UserRegistrationPayload(BaseModel):
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserUpdatePayload(BaseModel):
    email: str | None = Field(None, min_length=3, max_length=50)
    password: str | None = Field(None, min_length=8)
    old_password: str | None = Field(None, min_length=8)

class UserResponsePayload(BaseModel):
    id: int
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
