from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from core.models import Reservation
from schemas.reservation import ReservationCreate


async def get_all_reservations(session: AsyncSession) -> list[Reservation]:
    stmt = select(Reservation).order_by(Reservation.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_reservation(
    session: AsyncSession,
    reservation_create: ReservationCreate
) -> Reservation:
    reservation_time = reservation_create.reservation_time
    if reservation_time.tzinfo is not None:
        reservation_time = reservation_time.astimezone(timezone.utc).replace(tzinfo=None)

    existing = await get_conflicting_reservations(
        session=session,
        table_id=reservation_create.table_id,
        reservation_time=reservation_time,
        duration_minutes=reservation_create.duration_minutes
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Столик уже забронирован на это время"
        )
    reservation_data = reservation_create.model_dump()
    reservation_data['reservation_time'] = reservation_time.replace(tzinfo=None)

    reservation = Reservation(**reservation_data)
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)

    return reservation


async def get_conflicting_reservations(
    session: AsyncSession,
    table_id: int,
    reservation_time: datetime,
    duration_minutes: int
) -> list[Reservation]:
    if reservation_time.tzinfo is not None:
        reservation_time = reservation_time.replace(tzinfo=None)

    end_time = reservation_time + timedelta(minutes=duration_minutes)

    stmt = select(Reservation).where(
        and_(
            Reservation.table_id == table_id,
            Reservation.reservation_time < end_time,
            Reservation.reservation_time +
            (Reservation.duration_minutes * timedelta(minutes=1)) > reservation_time
        )
    )

    result = await session.scalars(stmt)
    return result.all()


async def reservation_delete(
    session: AsyncSession,
    reservation_id: int,
) -> None:
    reservation = await session.get(Reservation, reservation_id)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Бронирование {reservation_id} не найдено",
        )
    await session.delete(reservation)
    await session.commit()
