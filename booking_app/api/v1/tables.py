from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import tables as crud_tables
from core.models import db_helper
from schemas.table import TableCreate, TableRead

router = APIRouter(tags=["Tables"])


@router.get("", response_model=list[TableRead])
async def get_tables(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ]
):
    tables = await crud_tables.get_all_tables(session=session)
    return tables


@router.post("", response_model=TableRead)
async def create_table(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    table_create: TableCreate,
):
    table = await crud_tables.table_create(
        session=session,
        table_create=table_create,
    )
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    table_id: int,
):
    await crud_tables.table_delete(session=session, table_id=table_id)
    return None
