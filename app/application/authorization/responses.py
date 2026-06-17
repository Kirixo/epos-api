from datetime import datetime

from app.application.base import BaseResponse

class UserResponseValue(BaseResponse):
    email:str
    