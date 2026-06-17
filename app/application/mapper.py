from app.application.base import PaginationCommand
from app.domain.pagination import Pagination


class PaginationMapper:
    @staticmethod
    def pagination_from_command(command: PaginationCommand) -> Pagination:
        return Pagination(
            limit=command.limit,
            offset=command.offset,
            search=command.search,
        )
