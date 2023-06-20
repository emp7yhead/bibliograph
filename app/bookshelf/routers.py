from http import HTTPStatus
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwthandler import get_current_user
from app.bookshelf.models import Bookshelf
from app.bookshelf.schemas import BookshelfIn, BookshelfOut, BookshelfOutDb
from app.bookshelf.service import (
    add_bookshelf,
    get_bookshelf,
    get_bookshelves,
    remove_bookshelf,
    renew_bookshelf,
)
from app.database import get_session
from app.users.schemas import UserOut

bookshelf_router = APIRouter(prefix='/bookshelf', tags=['Bookshelves'])


@bookshelf_router.get(
    '',
    response_model=list[BookshelfOutDb],
    status_code=HTTPStatus.OK,
    description='Get user\'s bookshelves by id.',
)
async def read_user_bookshelves(
    user_id: Annotated[
        int,
        Query(
            ...,
            description="Id of user whose bookshelves you want to retrieve.",
            gt=0
        ),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[Bookshelf] | None:
    """Get user bookshelves."""
    bookshelves: Sequence[Bookshelf] = await get_bookshelves(session, user_id)
    return bookshelves


@bookshelf_router.get(
    '/{bookshelf_id}',
    response_model=BookshelfOutDb,
    status_code=HTTPStatus.OK,
    description='Get bookshelf by id.',
)
async def read_bookshelf(
    bookshelf_id: Annotated[
        int,
        Path(..., description="Id of bookshelf to get", gt=0)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Bookshelf | None:
    bookshelf: Bookshelf | None = await get_bookshelf(session, bookshelf_id)
    if not bookshelf:
        raise HTTPException(status_code=404, detail="Bookshelf not found")
    return bookshelf


@bookshelf_router.post(
    '',
    response_model=BookshelfOut,
    status_code=HTTPStatus.CREATED,
    description='Create new bookshelf for user. User must be authenticated.',
)
async def create_bookshelf(
    bookshelf: BookshelfIn,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Bookshelf:
    """Create new bookshelf for user."""
    new_bookshelf: Bookshelf = await add_bookshelf(
        session, bookshelf, current_user.id
    )
    return new_bookshelf


@bookshelf_router.put(
    '/{bookshelf_id}',
    response_model=BookshelfOutDb,
    status_code=HTTPStatus.OK,
    response_description='Bookshelf updated successfully',
    description='Update bookshelf by id. User must be authenticated.',
)
async def update_bookshelf(
    bookshelf_id: Annotated[
        int,
        Path(..., description="Id of bookshelf to update", gt=0)
    ],
    bookshelf: BookshelfIn,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Bookshelf | None:
    """Update user in database."""
    db_bookshelf: Bookshelf | None = await get_bookshelf(session, bookshelf_id)
    if not db_bookshelf:
        raise HTTPException(status_code=404, detail='Booskhelf not found')
    if db_bookshelf.user_id == current_user.id:
        try:
            updated_bookshelf: Bookshelf = await renew_bookshelf(
                session, bookshelf, bookshelf_id
            )
        except IntegrityError:
            raise HTTPException(status_code=409, detail='Username alredy taken')
        return updated_bookshelf
    raise HTTPException(status_code=403, detail="Not authorized to update")


@bookshelf_router.delete(
    '/{bookshelf_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_description='Successfully deleted bookshelf',
    description='Delete user bookshelf by id. User must be authenticated.',
)
async def delete_bookshelf(
    bookshelf_id: Annotated[
        int,
        Path(..., description="Delete bookshelf data by id", gt=0)
    ],
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Removes bookshelf from user."""
    bookshelf: Bookshelf | None = await get_bookshelf(session, bookshelf_id)
    if not bookshelf:
        return HTTPStatus.NO_CONTENT
    if bookshelf.user_id == current_user.id:
        await remove_bookshelf(session, bookshelf_id)
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=403, detail="Not authorized to delete")
