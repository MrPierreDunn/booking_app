from fastapi import APIRouter

from core.config import settings

from .reservations import router as reservations_router
from .tables import router as tables_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    tables_router,
    prefix=settings.api.v1.tables,
)
router.include_router(
    reservations_router,
    prefix=settings.api.v1.reservations,
)
