from __future__ import annotations

from typing import Any, Protocol


class ValueCodecProtocol(Protocol):
    def encode(self, payload: dict[str, Any]) -> dict[str, Any]: ...
    def decode(self, payload: dict[str, Any]) -> dict[str, Any]: ...
