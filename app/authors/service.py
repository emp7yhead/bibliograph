from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.authors.models import Author
from app.books.schemas import BookForDb


async def get_author_id(
    session: AsyncSession,
    book_info: BookForDb,
) -> int:
    author_id = await find_author_by_name(session, book_info)
    if not author_id:
        author_id = await add_author(session, book_info)
    return author_id


async def find_author_by_name(
    session: AsyncSession,
    book_info: BookForDb,
) -> Author | None:
    author_id = await session.execute(
        select(Author.id)
        .where(Author.name == ''.join(book_info.author)),
    )
    return author_id.scalar_one_or_none()


async def add_author(
    session: AsyncSession,
    book_info: BookForDb,
) -> Author:
    # NOTE: before add need to try find author
    author_id = await session.execute(
        insert(Author)
        .values(name=''.join(book_info.author))
        .returning(Author.id),
    )
    return author_id.scalar_one()
