from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.service import get_user_by_username

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password with password in database.

    Args:
        plain_password: password
        hashed_password: password stored in database

    Returns:
        bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password for database.

    Args:
        password: user password

    Returns:
        str
    """
    return pwd_context.hash(password)


async def validate_user(
    session: AsyncSession,
    user: OAuth2PasswordRequestForm = Depends(),
) -> User:
    """
    Verify that user exists and entered correct password.

    Args:
        session: database async session
        user: user data from auth form

    Returns:
        User
    """
    db_user: User | None = await get_user_by_username(session, user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    return db_user
