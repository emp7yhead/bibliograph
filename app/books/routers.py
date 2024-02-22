from http import HTTPStatus
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwthandler import get_current_user
from app.books.models import Book
from app.books.schemas import (
    BookForDb,
    BookIn,
    BookOut,
    BookOutDb,
    BookProgress,
)
from app.books.service import (
    add_book_info,
    get_all_books,
    get_book_by_id,
    remove_book,
    update_book,
)
from app.books.utils import get_book_info
from app.bookshelf.models import Bookshelf
from app.bookshelf.service import get_bookshelf
from app.database import get_session
from app.users.schemas import UserOut

books_router = APIRouter(prefix='/books', tags=['Books'])


@books_router.get(
    '/',
    response_model=list[BookOutDb],
    status_code=HTTPStatus.OK,
    description='Get all books from database.',
)
async def get_books(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[
        int | None,
        Query(description="Limit for list of books", ge=0),
    ] = None,
    offset: Annotated[
        int | None,
        Query(description="Offset for list of books", ge=0)
    ] = None,
) -> Sequence[Book]:
    """Get books info."""
    books: Sequence[Book] = await get_all_books(session, limit, offset)
    return books


@books_router.get(
    '/{book_id}',
    response_model=BookOutDb,
    status_code=HTTPStatus.OK,
    description='Get book info by id.',
)
async def get_book(
    book_id: Annotated[
        int,
        Path(..., description="Id of book to get", gt=0)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Book | None:
    """Get book info by book id."""
    book: Book | None = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.post(
    '',
    response_model=BookOut,
    status_code=HTTPStatus.CREATED,
    description='Create new book on bookshelf.',
)
async def create_book(
    book: BookIn,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Book:
    """Creates book and add it to bookshelf."""
    bookshelf: Bookshelf | None = await get_bookshelf(
        session, book.bookshelf_id
    )
    if not bookshelf:
        raise HTTPException(404, 'Bookshelf not found')
    if bookshelf.user_id == current_user.id:
        book_info: BookForDb = await get_book_info(book.title)
        return await add_book_info(session, book_info, book.bookshelf_id)
    raise HTTPException(status_code=403, detail="Not authorized to create")


@books_router.put(
    '/{book_id}',
    response_model=BookOutDb,
    status_code=HTTPStatus.OK,
    response_description='Book progress updated successfully',
    description='Update book progress by id. User must be authenticated.',
)
async def update_book_progress(
    book_id: Annotated[
        int,
        Path(..., description="Id of bookshelf to update", gt=0)
    ],
    book_progress: BookProgress,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Bookshelf | None:
    """Update user in database."""
    db_book: Book | None = await get_book_by_id(session, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail='Book not found')
    bookshelf: Bookshelf = await get_bookshelf(  # type: ignore
        session, db_book.bookshelf_id
    )
    if bookshelf.user_id == current_user.id:
        updated_book: Book = await update_book(
            session, book_id, book_progress
        )
        return updated_book
    raise HTTPException(status_code=403, detail="Not authorized to update")


@books_router.delete(
    '/{book_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_description='Successfully deleted bookshelf',
    description='Delete user bookshelf by id. User must be authenticated.',
)
async def delete_book(
    book_id: Annotated[
        int,
        Path(..., description="Delete book by id", gt=0)
    ],
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Removes book from db."""
    book: Book | None = await get_book_by_id(session, book_id)
    if not book:
        return HTTPStatus.NO_CONTENT
    bookshelf: Bookshelf = await get_bookshelf(  # type: ignore
        session, book.bookshelf_id
    )
    if bookshelf.user_id == current_user.id:
        await remove_book(session, book_id)
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=403, detail="Not authorized to delete")
