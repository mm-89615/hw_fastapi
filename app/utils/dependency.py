import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import TOKEN_TTL_SEC
from db import Session
from models import Token


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]


async def get_token(
    x_token: Annotated[uuid.UUID, Header()],
    session: SessionDependency
) -> Token:
    token_query = select(Token).where(
        Token.token == x_token,
        Token.created_at >= datetime.now() - timedelta(seconds=TOKEN_TTL_SEC)
    )
    token = await session.scalar(token_query)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


TokenDependency = Annotated[Token, Depends(get_token, use_cache=True)]
