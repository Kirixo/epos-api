import logging
from collections.abc import Awaitable, Callable, Sequence
from typing import Any, cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exception import BaseBoundaryException
from app.core.exception_resolver import MessageResolver
from app.infra.exception import BaseInfraException


FastAPIExceptionHandler = Callable[[Request, Any], Awaitable[JSONResponse]]
logger = logging.getLogger(__name__)


def build_exception_handler() -> FastAPIExceptionHandler:
    resolver = MessageResolver()

    async def handler(request: Request, exc: Exception) -> JSONResponse:
        event_name = "internal"
        event_context = {}
        if isinstance(exc, BaseBoundaryException):
            event_name = exc.message_key
            event_context = exc.context
            msg = resolver.resolve(exc.message_key, exc.context)
            code = getattr(exc, "code", 400)
        elif isinstance(exc, BaseInfraException):
            msg = resolver.resolve("internal", {})
            code = 503
        else:
            msg = resolver.resolve("internal", {})
            code = 500

        logger.error(
            "Stub exception handler received %s: %s",
            type(exc).__name__,
            str(exc),
            extra={
                "event_name": event_name,
                "exception_context": event_context,
            },
        )

        if settings.debug_mode:
            return JSONResponse(
                status_code=code,
                content={
                    "detail": {
                        "msg": msg,
                        "type": type(exc).__name__,
                        "extra": {
                            "event_name": event_name,
                            "exception_context": event_context,
                        },
                    },
                    "context": {
                        **event_context,
                    },
                },
            )
        return JSONResponse(
            status_code=code,
            content={"detail": msg},
        )

    return handler


def _sanitize_validation_errors(errors: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    sanitized_errors: list[dict[str, Any]] = []
    for error in errors:
        sanitized_error = dict(error)
        sanitized_error.pop("input", None)
        sanitized_errors.append(sanitized_error)
    return sanitized_errors


async def build_validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    validation_error = cast(RequestValidationError, exc)
    return JSONResponse(
        status_code=422,
        content={"detail": _sanitize_validation_errors(validation_error.errors())},
    )


def register_fastapi_exception_handlers(
    app: FastAPI,
) -> FastAPI:
    app.add_exception_handler(RequestValidationError, build_validation_exception_handler)
    app.add_exception_handler(Exception, build_exception_handler())
    return app
