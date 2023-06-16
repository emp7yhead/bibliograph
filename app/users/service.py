from typing import Sequence

from passlib.context import CryptContext
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemas import UserIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_all_users(
    session: AsyncSession, offset: int | None, limit: int | None
) -> Sequence[User]:
    users = await session.execute(
        select(User).limit(limit).offset(offset)
    )
    return users.scalars().all()


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    db_user = await session.execute(
        select(User).where(
            User.id == user_id
        )
    )
    return db_user.scalar_one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    db_user = await session.execute(
        select(User).where(User.username == username)
    )
    return db_user.scalar_one_or_none()


async def add_user(session: AsyncSession, user: UserIn) -> User:
    user.password = pwd_context.encrypt(user.password)

    db_user = await session.execute(
        insert(User).values(**user.dict()).returning(User)
    )
    await session.commit()
    return db_user.scalar_one()


async def renew_user(session: AsyncSession, user: UserIn, id: int) -> User:
    updated_user = await session.execute(
        update(User).where(User.id == id).values(
            password=user.password,
            username=user.username,
            email=user.email,
        ).execution_options(synchronize_session="evaluate").returning(User)
    )
    await session.commit()
    return updated_user.scalar_one()


async def remove_user(session: AsyncSession, user_id: int) -> User:
    deleted_user = await session.execute(
        delete(User).
        where(User.id == user_id).
        execution_options(synchronize_session="fetch").returning(User)
    )
    await session.commit()
    return deleted_user.scalar_one_or_none()
