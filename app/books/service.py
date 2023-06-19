from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.books.models import Author, Book, Sentence
from app.books.schemas import BookForDb


async def add_book_info(
    session: AsyncSession, book_info: BookForDb, bookshelf_id: int,
) -> Book:
    """Add book to bookshelf.

    Args:
        session: database async session
        book_info: book info in pydantic model
        bookshelf_id: id bookshelf where book will be placed

    Returns: Book
    """
    # Note: Add first search already existed book
    author_id = await add_author(session, book_info)
    new_book = await add_book(session, book_info, bookshelf_id, author_id)
    if book_info.first_sentence:
        await add_sentence(
            session, new_book.id, book_info.first_sentence
        )
    await session.flush()
    await session.commit()
    return new_book


async def add_author(session: AsyncSession, book_info: BookForDb):
    # NOTE: before add need to try find author
    author_id = await session.execute(
        insert(Author)
        .values(name=''.join(book_info.author))
        .returning(Author.id)
    )
    return author_id.scalar_one()


async def add_sentence(session: AsyncSession, book_id: int, sentence: list):
    return await session.execute(
            insert(Sentence)
            .values(
                book_id=book_id,
                content=''.join(sentence))
            .returning(Sentence.id)
        )


async def add_book(
    session: AsyncSession,
    book_info: BookForDb,
    bookshelf_id: int,
    author_id: int,
) -> Book:
    # NOTE: add check if book already exist
    new_book = await session.execute(
        insert(Book)
        .values(
            title=book_info.title,
            author_id=author_id,
            total_pages=book_info.total_pages,
            bookshelf_id=bookshelf_id,
        )
        .returning(Book)
    )
    return new_book.scalar_one()


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book | None:
    """
    Get book by id

    Args:
        session: database async session
        book_id: id of book to get

    Returns: Book | None
    """
    book = await session.execute(
        select(Book)
        .options(selectinload(Book.author))
        .where(Book.id == book_id)
    )
    return book.scalar_one_or_none()
