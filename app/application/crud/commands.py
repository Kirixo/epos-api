from __future__ import annotations

from pydantic import Field

from app.application.base import FlexibleCommand, PaginationCommand

class GetCrudCommand(FlexibleCommand):
    user_id: int
    workspace_id: int
    item_id: int
    
class ListCrudCommand(PaginationCommand):
    user_id: int
    workspace_id: int
    
class DeleteCrudCommand(FlexibleCommand):
    user_id: int
    workspace_id: int
    item_id: int
    
class UpdateCrudCommand(FlexibleCommand):
    user_id: int
    workspace_id: int
    item_id: int
    item_name: str | None
    item_value: str | None
    
class CreateCrudCommand(FlexibleCommand):
    user_id: int
    workspace_id: int
    item_name: str
    item_value: str