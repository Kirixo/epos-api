from fastapi import APIRouter

from app.api.v1.crud.crud import router as batch_router

router = APIRouter(prefix="/v1")
router.include_router(batch_router, prefix="/crud")

# router.include_router(..., prefix="/...")