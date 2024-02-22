from http import HTTPStatus
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwthandler import get_current_user
from app.database import get_session
from app.users.models import User
from app.users.schemas import UserIn, UserOut, UserOutDb
from app.users.service import get_all_users, get_user, remove_user, renew_user

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get(
    '',
    response_model=list[UserOutDb],
    status_code=HTTPStatus.OK,
    description='Get all users from database',
)
async def read_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[
        int | None,
        Query(description="Limit for list of users", ge=0),
    ] = None,
    offset: Annotated[
        int | None,
        Query(description="Offset for list of users", ge=0)
    ] = None,
) -> Sequence[User]:
    """Get all user from database."""
    users: Sequence[User] = await get_all_users(session, limit, offset)
    return users


@user_router.get(
    '/{user_id}',
    response_model=UserOutDb,
    status_code=HTTPStatus.OK,
    description='Get user by id.',
)
async def read_user(
    user_id: Annotated[
        int,
        Path(..., description="Id of user to get", gt=0)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User | None:
    """Get user from database by specified id."""
    db_user: User | None = await get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@user_router.put(
    '/{user_id}',
    response_model=UserOut,
    status_code=HTTPStatus.OK,
    response_description='User updated successfully',
    description='Update user by id. User must be authenticated.',
)
async def update_user(
    user_id: Annotated[
        int,
        Path(..., description="Id of user to update", gt=0)
    ],
    user: UserIn,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User | None:
    """Update user in database."""
    db_user: User | None = await get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    if user_id == current_user.id:
        try:
            updated_user: User = await renew_user(session, user, user_id)
        except IntegrityError:
            raise HTTPException(status_code=409, detail='Username alredy taken')
        return updated_user
    raise HTTPException(status_code=403, detail="Not authorized to update")


@user_router.delete(
    '/{user_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_description='Successfully deleted user',
    description='Delete user by id. User must be authenticated.',
)
async def delete_user(
    user_id: Annotated[
        int,
        Path(..., description="Id of user to delete", gt=0)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[UserOut, Depends(get_current_user)],
):
    """Remove user from database by specified id."""
    db_user: User | None = await get_user(session, user_id)
    if not db_user:
        return HTTPStatus.NO_CONTENT
    if user_id == current_user.id:
        await remove_user(session, user_id)
        return HTTPStatus.NO_CONTENT
    raise HTTPException(status_code=403, detail="Not authorized to delete")
