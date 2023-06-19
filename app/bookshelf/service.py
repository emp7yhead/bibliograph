from typing import Sequence

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.bookshelf.models import Bookshelf
from app.bookshelf.schemas import BookshelfIn


async def get_bookshelves(
    session: AsyncSession, user_id: int
) -> Sequence[Bookshelf]:
    """
    Get all bookshelves for user

    Args:
        session: database async session
        user_id: id of user

    Returns: Sequence[Bookshelf]
    """
    bookshelves = await session.execute(
        select(Bookshelf).where(Bookshelf.user_id == user_id)
    )
    return bookshelves.scalars().all()


async def get_bookshelf(
    session: AsyncSession, bookshelf_id: int
) -> Bookshelf | None:
    """
    Get bookshelf by id

    Args:
        session: database async session
        bookshelf_id: id of bookshelf to get

    Returns: Bookshelf
    """
    bookshelves = await session.execute(
        select(Bookshelf)
        .options(selectinload(Bookshelf.books))
        .where(Bookshelf.id == bookshelf_id)
    )
    return bookshelves.scalar_one_or_none()


async def add_bookshelf(
    session: AsyncSession, bookshelf: BookshelfIn, user_id: int,
) -> Bookshelf:
    """
    Add bookshelf for user

    Args:
        session: database async session
        bookshelf: bookshelf data
        user_id: id of user

    Returns: Bookshelf
    """
    new_bookshelf = await session.execute(
        insert(Bookshelf)
        .values(**bookshelf.dict(), user_id=user_id)
        .returning(Bookshelf)
    )
    await session.commit()
    return new_bookshelf.scalar_one()


async def renew_bookshelf(
    session: AsyncSession, bookshelf: BookshelfIn, bookshelf_id: int,
) -> Bookshelf:
    """
    Update bookshelf by id.

    Args:
        session: database async session
        bookshelf: bookshelf data
        bookshelf_id: id of bookshelf

    Returns: Bookshelf
    """
    updated_bookshelf = await session.execute(
        update(Bookshelf).where(Bookshelf.id == bookshelf_id).values(
            title=bookshelf.title,
        ).execution_options(synchronize_session="evaluate").returning(Bookshelf)
    )
    await session.commit()
    return updated_bookshelf.scalar_one()


async def remove_bookshelf(
    session: AsyncSession, bookshelf_id: int
) -> Bookshelf | None:
    """
    Remove bookshelf from database

    Args:
        session: database async session
        bookshelf_id: id of bookshelf

    Returns: Bookshelf
    """
    bookshelf = await session.execute(
        delete(Bookshelf).
        where(Bookshelf.id == bookshelf_id).
        execution_options(synchronize_session="fetch").returning(Bookshelf)
    )
    await session.commit()
    return bookshelf.scalar_one_or_none()
