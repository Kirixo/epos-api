from fastapi import APIRouter

from app.api.v1.sync.router import router as sync_router
from app.api.v1.users.router import router as users_router
from app.api.v1.auth.router import router as auth_router

router = APIRouter(prefix="/v1")
router.include_router(users_router, prefix="/users")
router.include_router(auth_router, prefix="/auth")
router.include_router(sync_router, prefix="/sync")
