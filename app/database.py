import contextlib
from collections.abc import AsyncIterator
from typing import Any

from pydantic import PostgresDsn
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.exceptions import DatabaseSessionManagerError
from app.settings import settings

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(
        self,
        connection_uri: PostgresDsn,
        engine_kwargs: dict[str, Any],
    ) -> None:
        self._engine = create_async_engine(
            connection_uri,
            poolclass=NullPool,
            **engine_kwargs,
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False,
        )

    def init(self, connection_uri: PostgresDsn) -> None:
        self._engine = create_async_engine(connection_uri, poolclass=NullPool)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine,
        )

    async def close(self) -> None:
        if self._engine is None:
            raise DatabaseSessionManagerError
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseSessionManagerError

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseSessionManagerError

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager(
    settings.SQLALCHEMY_DATABASE_URI, {'echo': True},
)
