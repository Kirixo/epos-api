from typing import Mapping

from app.application.authorization.responses import UserResponseValue
from app.domain.user.entity import UserEntity



class AuthenticationCommandsMapper:
    
    @classmethod
    def user_domain_to_value(cls, domain: UserEntity) -> UserResponseValue:
        return UserResponseValue(
            email=domain.email
        )
    