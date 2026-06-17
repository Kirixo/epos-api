from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any, TypeVar

from pydantic import BaseModel

TCommand = TypeVar("TCommand", bound=BaseModel)
TResponseValue = TypeVar("TResponseValue", bound=BaseModel)


class GeneralMapper:
    @staticmethod
    def to_dict(*payloads: BaseModel, **extra: object) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for payload in payloads:
            data.update(payload.model_dump(exclude_none=True))
        data.update({key: value for key, value in extra.items() if value is not None})
        return data

    @staticmethod
    def command_payload_to_command(
        command_type: type[TCommand],
        payload: Mapping[str, object],
    ) -> TCommand:
        return command_type.model_validate(dict(payload))

    @staticmethod
    def domain_to_response_value(
        response_value_type: type[TResponseValue],
        domain_payload: Mapping[str, object],
        **extra: object,
    ) -> TResponseValue:
        payload = deepcopy(dict(domain_payload))
        payload.update({key: value for key, value in extra.items() if value is not None})
        return response_value_type.model_validate(payload)
