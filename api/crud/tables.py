from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from core.models import Table
from schemas.table import TableCreate


async def get_all_tables(session: AsyncSession) -> list[Table]:
    logger.info("Try to getting all tables")
    try:
        stmt = select(Table).order_by(Table.id)
        result = await session.scalars(stmt)
        tables = result.all()
        logger.info(f"Found {len(tables)} tables")
        return tables
    except Exception as error:
        logger.error(f"Error getting tables {str(error)}")
        raise


async def table_create(
        session: AsyncSession,
        table_create: TableCreate,
) -> Table:
    logger.info(f"Creating new table: {table_create.model_dump_json()}")
    try:
        table = Table(**table_create.model_dump())
        session.add(table)
        await session.commit()
        logger.info(f"Sucsessfully create table № {table.id}")
        return table
    except Exception as error:
        logger.error(f"Faild to create table {str(error)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create table"
        )


async def table_delete(
    session: AsyncSession,
    table_id: int,
) -> None:
    logger.info(f"Attempting to delete table № {table_id}")
    try:
        table = await session.get(Table, table_id)
        if table is None:
            logger.warning(f"Table № {table_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Столик {table_id} не найден",
            )
        await session.delete(table)
        await session.commit()
        logger.info(f"Successfully deleted table № {table_id}")
    except HTTPException:
        raise
    except Exception as error:
        logger.error(
            f"Failed to delete table № {table_id} {str(error)}", exc_info=True
        )
        raise
