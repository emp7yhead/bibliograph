from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwthandler import get_current_user
from app.books.models import Book
from app.books.schemas import BookForDb, BookIn, BookOut, BookOutDb
from app.books.service import add_book_info, get_book_by_id
from app.books.utils import get_book_info
from app.bookshelf.models import Bookshelf
from app.bookshelf.service import get_bookshelf
from app.database import get_session
from app.users.schemas import UserOut

books_router = APIRouter(prefix='/books', tags=['Books'])


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
):
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
):
    bookshelf: Bookshelf | None = await get_bookshelf(
        session, book.bookshelf_id
    )
    if not bookshelf:
        raise HTTPException(404, 'Bookshelf not found')
    if bookshelf.user_id == current_user.id:
        book_info: BookForDb = await get_book_info(book.title)
        return await add_book_info(session, book_info, book.bookshelf_id)
    raise HTTPException(status_code=403, detail="Not authorized to create")
