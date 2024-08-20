from collections.abc import AsyncGenerator
from typing import Any

from app.database import sessionmanager


async def get_session() -> AsyncGenerator[Any, Any]:
    async with sessionmanager.session() as session:
        yield session
