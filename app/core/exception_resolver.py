from typing import Any, Dict


class MessageResolver:
    CATALOG: dict[str, str] = {
        "internal": "Internal server error",
        "email_exists": "Email already exists",
        "invalid_old_password": "Invalid old password",
        "user_not_found": "User not found",
        "invalid_token": "Invalid or expired token",
        "invalid_credentials": "Invalid email or password",
        "authorization.denied": "Access denied",
        }

    def resolve(self, key: str, context: Dict[str, Any]) -> str:
        
        template = self.CATALOG.get(key, "Internal server error")
        
        try:
            template = template.format(**context)
        finally:
            template = template
             
        return template
     
