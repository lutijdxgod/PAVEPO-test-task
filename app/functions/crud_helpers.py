from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.models.database import db_helper as db


async def get_single_entity_by_field(
    entity: Table,
    field: InstrumentedAttribute,
    value: Any,
    session: AsyncSession,
):
    query = select(entity).where(field == value)
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


async def get_entity_by_field(
    entity: Table,
    field: InstrumentedAttribute,
    value: Any,
    session: AsyncSession,
):
    query = select(entity).where(field == value)
    query_result = await session.scalars(query)
    result = query_result.all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


async def get_entity_by_multiple_fields(
    entity: Table,
    fields: list[InstrumentedAttribute],
    session: AsyncSession,
):
    query = select(entity).where(*fields)
    query_result = await session.scalars(query)
    result = query_result.all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


async def get_entity_by_field_nullable(
    entity: Table,
    field: InstrumentedAttribute,
    value: Any,
    session: AsyncSession,
):
    query = select(entity).where(field == value)
    query_result = await session.scalars(query)
    result = query_result.all()

    return result


async def get_entity_by_multiple_fields_nullable(
    entity: Table,
    fields: list[InstrumentedAttribute],
    session: AsyncSession,
):
    query = select(entity).where(*fields)
    query_result = await session.scalars(query)
    result = query_result.all()

    return result
