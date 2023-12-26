import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from orm.entities import Base

load_dotenv()

_pg_user = os.environ.get('POSTGRES_USER')
_pg_pass = os.environ.get('POSTGRES_PASSWORD')
_pg_host = os.environ.get('POSTGRES_HOST')
_pg_db = os.environ.get('POSTGRES_DB')
_pg_port = os.environ.get("POSTGRES_PORT")

engine = create_async_engine(f"postgresql+asyncpg://{_pg_user}:{_pg_pass}@{_pg_host}:{_pg_port}/{_pg_db}")

make_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
