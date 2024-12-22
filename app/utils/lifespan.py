from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import init_orm, close_orm


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_orm()
    yield
    await close_orm()
