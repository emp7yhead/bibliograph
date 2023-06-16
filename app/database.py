from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.settings import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

async_session: sessionmaker[Session] = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    """Dependency to create future sessions."""
    async with async_session() as session:
        yield session
