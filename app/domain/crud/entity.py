from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass
class CrudEntity:
    id: int
    item_name: str
    item_value: str
    updated_at: datetime | None = None
    created_at: datetime | None = None
    
    def update(self, *,
        item_name: str | None = None, 
        item_value: str | None = None, 
    ) -> None:
        if item_name is not None:
            self.item_name = item_name
        if item_value is not None:
            self.item_value = item_value
        
        self.updated_at = datetime.now(UTC)
        
    @classmethod
    def create(
        cls,
        *,
        item_name: str,
        item_value: str,
    ) -> "CrudEntity":
        return CrudEntity(
            id=uuid4().int,
            item_name=item_name,
            item_value=item_value
        )