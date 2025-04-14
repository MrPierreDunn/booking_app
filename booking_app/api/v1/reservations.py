from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..crud import reservations as crud_reservation
from core.models import db_helper
from schemas.reservation import ReservationCreate, ReservationRead

router = APIRouter(tags=["Reservations"])


@router.get("", response_model=list[ReservationRead])
async def get_reservations(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ]
):
    reservations = await crud_reservation.get_all_reservations(session=session)
    return reservations


@router.post("", response_model=ReservationRead)
async def create_reservation(
    reservation_create: ReservationCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    try:
        return await crud_reservation.create_reservation(
            session=session,
            reservation_create=reservation_create
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    reservation_id: int,
):
    await crud_reservation.reservation_delete(session=session, reservation_id=reservation_id)
    return None
