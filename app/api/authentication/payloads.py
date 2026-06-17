from pydantic import BaseModel, Field


class UserRegistrationSchemaPayload(BaseModel):
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    name: str = Field(min_length=2, max_length=100)
    surname: str = Field(min_length=2, max_length=100)
    nickname: str = Field(min_length=2, max_length=32)