from typing import Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import ORM_OBJ, ORM_CLS


async def add_item(session: AsyncSession, item: ORM_OBJ):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Record already exists")


async def get_item_by_id(session: AsyncSession,
        orm_cls: ORM_CLS,
        item_id: int) -> ORM_OBJ:
    orm_object = await session.get(orm_cls, item_id)
    if not orm_object:
        raise HTTPException(status_code=404, detail="Record not found")
    return orm_object


async def delete_item(session: AsyncSession, item: ORM_OBJ) -> None:
    await session.delete(item)
    await session.commit()


async def get_items_by_filters(session: AsyncSession,
        orm_cls: ORM_CLS,
        filters: dict[str, Any] | None = None) -> Sequence[ORM_OBJ]:
    query = select(orm_cls)
    if filters:
        for field, value in filters.items():
            if hasattr(orm_cls, field):
                query = query.where(getattr(orm_cls, field) == value)
    result = await session.execute(query)
    items = result.scalars().all()
    if not items:
        raise HTTPException(status_code=404, detail="Records not found")
    return items
