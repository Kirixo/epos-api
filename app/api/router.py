from fastapi import APIRouter

from app.api.v1.router import router as v1_router
from app.api.authentication.authentication import router as authentication_router

router = APIRouter()
router.include_router(v1_router)
router.include_router(authentication_router)
