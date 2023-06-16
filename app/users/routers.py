from http import HTTPStatus
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwthandler import get_current_user
from app.database import get_session
from app.users.models import User
from app.users.schemas import UserIn, UserOut
from app.users.service import (
    add_user,
    get_all_users,
    get_user,
    get_user_by_username,
    remove_user,
    renew_user,
)

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get(
    '/',
    response_model=list[UserOut],
    status_code=HTTPStatus.OK,
)
async def read_users(
    limit: int | None = None,
    offset: int | None = None,
    session: AsyncSession = Depends(get_session),
) -> Sequence[User]:
    users: Sequence[User] = await get_all_users(session, limit, offset)
    return users


@user_router.post(
    '/',
    response_model=UserOut,
    status_code=HTTPStatus.CREATED,
)
async def create_user(
    user: UserIn,
    session: AsyncSession = Depends(get_session),
) -> User:
    db_user = await get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )
    new_user: User = await add_user(session, user)
    return new_user


@user_router.get(
    '/{user_id}',
    response_model=UserOut,
    status_code=HTTPStatus.OK,
)
async def read_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> User | None:
    db_user: User = await get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@user_router.put(
    '/{user_id}',
    response_model=UserOut,
    status_code=HTTPStatus.OK,
    response_description='User updated successfully',
)
async def update_user(
    user_id: int,
    user: UserIn,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> User | None:
    db_user: User = await get_user(session, user_id)
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
    response_model=UserOut,
    status_code=HTTPStatus.OK,
    response_description='Successfully deleted user'
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(get_current_user),
) -> User:
    db_user: User = await get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id == current_user.id:
        return await remove_user(session, user_id)
    raise HTTPException(status_code=403, detail="Not authorized to delete")
