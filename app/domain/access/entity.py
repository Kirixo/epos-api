from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class UserWorkspaceAccessEntity:
    user_id: int
    workspace_id: int
    assigned_at: datetime | None = None

    def update(
        self,
        *,
        user_id: int | None = None,
        workspace_id: int | None = None,
        assigned_at: datetime | None = None,
    ) -> None:
        if user_id is not None:
            self.user_id = user_id
        if workspace_id is not None:
            self.workspace_id = workspace_id
        self.assigned_at = assigned_at if assigned_at is not None else datetime.now(UTC)
