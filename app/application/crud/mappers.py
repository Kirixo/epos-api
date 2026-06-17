from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict
from typing import Any

from app.application.crud.commands import *
from app.application.crud.responses import CrudValue
from app.core.utils.general_mapper import GeneralMapper
from app.domain.crud.entity import CrudEntity


class CrudCommandMapper:
    @classmethod
    def create_from_transport(cls, payload: Mapping[str, object]) -> CreateCrudCommand:
        return GeneralMapper.command_payload_to_command(CreateCrudCommand, payload)
    
    @classmethod
    def get_from_transport(cls, payload: Mapping[str, object]) -> GetCrudCommand:
        return GeneralMapper.command_payload_to_command(GetCrudCommand, payload)
    
    @classmethod
    def list_from_transport(cls, payload: Mapping[str, object]) -> ListCrudCommand:
        return GeneralMapper.command_payload_to_command(ListCrudCommand, payload)
    
    @classmethod
    def update_from_transport(cls, payload: Mapping[str, object]) -> UpdateCrudCommand:
        return GeneralMapper.command_payload_to_command(UpdateCrudCommand, payload)

    @classmethod
    def delete_from_transport(cls, payload: Mapping[str, object]) -> DeleteCrudCommand:
        return GeneralMapper.command_payload_to_command(DeleteCrudCommand, payload)


class CrudResponseMapper:
    @classmethod
    def crud_to_value(
        cls,
        entity: CrudEntity,
    ) -> CrudValue:
        return CrudValue(
            id=entity.id,
            item_name=entity.item_name,
            item_value=entity.item_value,
            updated_at=entity.updated_at
        )
