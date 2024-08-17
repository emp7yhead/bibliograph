from httpx import AsyncClient
from sqlalchemy import NullPool
from app.database import get_session

from app.main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/test"


engine = create_async_engine(
    DATABASE_URL, future=True, echo=True, poolclass=NullPool
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@app.on_event('startup')
async def create_db():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)


@app.on_event('shutdown')
async def drop_db():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)


async def get_test_session():
    async with async_session() as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

client = AsyncClient(app=app, base_url="http://test")
