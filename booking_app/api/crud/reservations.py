from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from core.models import Reservation
from schemas.reservation import ReservationCreate


async def get_all_reservations(session: AsyncSession) -> list[Reservation]:
    logger.info("Getting all reservations")
    try:
        stmt = select(Reservation).order_by(Reservation.id)
        result = await session.scalars(stmt)
        reservations = result.all()
        logger.info(f"Found {len(reservations)} reservations")
        return reservations
    except Exception as error:
        logger.error(f"Error getting reservations: {str(error)}")
        raise


async def create_reservation(
    session: AsyncSession,
    reservation_create: ReservationCreate
) -> Reservation:
    logger.info(
        "Attempting to create reservation for "
        f"table {reservation_create.table_id} "
        f"at {reservation_create.reservation_time} "
        f"for {reservation_create.duration_minutes} minutes"
    )
    try:
        reservation_time = reservation_create.reservation_time
        if reservation_time.tzinfo is not None:
            reservation_time = (
                reservation_time.astimezone(timezone.utc).replace(tzinfo=None)
            )

        logger.debug("Checking for conflicting reservations")
        existing = await get_conflicting_reservations(
            session=session,
            table_id=reservation_create.table_id,
            reservation_time=reservation_time,
            duration_minutes=reservation_create.duration_minutes
        )

        if existing:
            logger.warning(
                f"Conflict found for table {reservation_create.table_id} "
                f"at {reservation_time}"
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Столик уже забронирован на это время"
            )
        reservation_data = reservation_create.model_dump()
        reservation_data['reservation_time'] = (
            reservation_time.replace(tzinfo=None)
        )
        reservation = Reservation(**reservation_data)

        session.add(reservation)
        await session.commit()
        await session.refresh(reservation)

        logger.info(
            f"Successfully created reservation with ID {reservation.id}"
        )
        return reservation
    except HTTPException:
        raise
    except Exception as error:
        logger.error(
            f"Failed to create reservation {str(error)}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def get_conflicting_reservations(
    session: AsyncSession,
    table_id: int,
    reservation_time: datetime,
    duration_minutes: int
) -> list[Reservation]:
    logger.debug(
        f"Checking conflicts for table {table_id} "
        f"at {reservation_time} for {duration_minutes} minutes"
    )
    try:
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
        conflicts = result.all()

        if conflicts:
            logger.debug(f"Found {len(conflicts)} conflicts reservations")
        return conflicts
    except Exception as error:
        logger.error(f"Error checking conflicts: {str(error)}", exc_info=True)
        raise


async def reservation_delete(
    session: AsyncSession,
    reservation_id: int,
) -> None:
    logger.info(f"Attempting to delete reservation {reservation_id}")
    reservation = await session.get(Reservation, reservation_id)
    try:
        if reservation is None:
            logger.warning(f"Reservation {reservation_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Бронирование {reservation_id} не найдено",
            )
        await session.delete(reservation)
        await session.commit()
        logger.info(f"Successfully deleted reservation {reservation_id}")
    except HTTPException:
        raise
    except Exception as error:
        logger.error(
            f"Failed to delete reservation {reservation_id}: "
            f"{str(error)}", exc_info=True
        )
        raise
