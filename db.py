from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import db_engine_url
from orm.entities import Base

engine = create_async_engine(db_engine_url)
make_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def create_tables_at_start(_: FastAPI):
    # Создание таблиц в БД
    await create_tables()
    yield
