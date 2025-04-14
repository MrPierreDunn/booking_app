from fastapi import APIRouter

from .v1 import router as table_router

router = APIRouter()
router.include_router(
    table_router,
)
