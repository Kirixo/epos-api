from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import settings
from app.di.exceptions_handler import register_fastapi_exception_handlers

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Base FastAPI project with API versioning and Docker support.",
)

app.include_router(api_router)

register_fastapi_exception_handlers(app)