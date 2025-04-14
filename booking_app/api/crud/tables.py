from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.table import TableCreate

from core.models import Table


async def get_all_tables(session: AsyncSession) -> list[Table]:
    stmt = select(Table).order_by(Table.id)
    result = await session.scalars(stmt)
    return result.all()


async def table_create(
        session: AsyncSession,
        table_create: TableCreate,
) -> Table:
    table = Table(**table_create.model_dump())
    session.add(table)
    await session.commit()
    return table


async def table_delete(
    session: AsyncSession,
    table_id: int,
) -> None:
    table = await session.get(Table, table_id)
    if table is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Столик {table_id} не найден",
        )
    await session.delete(table)
    await session.commit()
