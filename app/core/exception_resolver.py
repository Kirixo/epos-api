from typing import Any, Dict


class MessageResolver:
    CATALOG: dict[str, str] = {
        "internal": "Internal server error",
        }

    def resolve(self, key: str, context: Dict[str, Any]) -> str:
        
        template = self.CATALOG.get(key, "Internal server error")
        
        try:
            template = template.format(**context)
        finally:
            template = template
             
        return template
     
