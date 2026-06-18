from dataclasses import dataclass
from datetime import UTC, datetime

@dataclass
class UserSettingsEntity:
    user_id: int
    theme: str
    language: str

    def update(self, *, theme: str | None = None, language: str | None = None) -> None:
        if theme is not None:
            self.theme = theme
        if language is not None:
            self.language = language
