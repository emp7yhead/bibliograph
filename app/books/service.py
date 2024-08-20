from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.authors.service import get_author_id
from app.books.models import Book, ReadStatus
from app.books.schemas import BookForDb, BookProgress
from app.sentences.service import add_sentence


async def get_all_books(
    session: AsyncSession, offset: int | None, limit: int | None,
) -> Sequence[Book]:
    """
    Get all books from database

    Args:
        session: database async session
        offset: offset for query
        limit: limit for query

    Returns: Sequence[Book]
    """
    books = await session.execute(
        select(Book)
        .limit(limit)
        .offset(offset),
    )
    return books.scalars().all()


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
    author_id = await get_author_id(session, book_info)
    new_book = await add_book(session, book_info, bookshelf_id, author_id)
    if book_info.first_sentence:
        await add_sentence(
            session, new_book.id, book_info.first_sentence,
        )
    await session.flush()
    await session.commit()
    return new_book


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
        .returning(Book),
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
        .where(Book.id == book_id),
    )
    return book.scalar_one_or_none()


async def update_book(
    session: AsyncSession, book_id: int, book_progress: BookProgress,
) -> Book:
    """
    Get book by id

    Args:
        session: database async session
        book_id: id of book to update
        books_progress: number of readed pages

    Returns: Book | None
    """
    book: Book = await get_book_by_id(session, book_id)  # type: ignore
    if not book_progress.readed_pages:
        updated_book = await session.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(
                status=ReadStatus.IN_PROGRESS,
                started_at=datetime.now(),
            )
            .returning(Book),
        )
    elif book.readed_pages == book_progress.readed_pages:
        updated_book = await session.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(
                status=ReadStatus.FINISHED,
                finished_at=datetime.now(),
                readed_pages=book_progress.readed_pages,
            )
            .returning(Book),
        )
    elif book.progress == ReadStatus.IN_PROGRESS:
        updated_book = await session.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(readed_pages=book_progress.readed_pages)
            .returning(Book),
        )
    else:
        updated_book = await session.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(
                status=ReadStatus.IN_PROGRESS,
                started_at=datetime.now(),
                readed_pages=book_progress.readed_pages,
            )
            .returning(Book),
        )
    await session.commit()
    return updated_book.scalar_one()


async def remove_book(
    session: AsyncSession, book_id: int,
) -> Book | None:
    """
    Remove book from database

    Args:
        session: database async session
        book_id: book id

    Returns: Book
    """
    bookshelf = await session.execute(
        delete(Book)
        .where(Book.id == book_id)
        .execution_options(synchronize_session='fetch')
        .returning(Book),
    )
    await session.commit()
    return bookshelf.scalar_one_or_none()
