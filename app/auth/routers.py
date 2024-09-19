from datetime import timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwthandler import create_access_token
from app.auth.service import validate_user
from app.dependencies import get_session
from app.settings import settings
from app.users.schemas import UserIn, UserOut
from app.users.service import add_user, get_user_by_username

if TYPE_CHECKING:
    from app.users.models import User

auth_router = APIRouter(tags=['Auth'])


@auth_router.post(
    '/register',
    response_model=UserOut,
    status_code=HTTPStatus.CREATED,
    description='Create new user.',
)
async def create_user(
    user: UserIn,
    session: AsyncSession = Depends(get_session),
) -> UserOut:
    db_user = await get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered',
        )
    new_user: User = await add_user(session, user)
    return new_user


@auth_router.post(
    '/login',
    status_code=HTTPStatus.OK,
    description='Verify user and gives access token.',
)
async def login(
    user: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Response:
    """Login as user. Verify user and gives access token."""
    user = await validate_user(session, user)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires,
    )
    token = jsonable_encoder(access_token)
    content = {'message': "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        'Authorization',
        value=f'Bearer {token}',
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite='lax',
        secure=False,
    )

    return response
