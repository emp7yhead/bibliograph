from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenData
from app.dependencies import get_session
from app.settings import settings
from app.users.models import User
from app.users.service import get_user_by_username


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str | None = None,
        scopes: dict | None = None,
        *,
        auto_error: bool =True,
    ) -> None:
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={
                'tokenUrl': token_url,
                'scopes': scopes,
            },
        )
        super().__init__(
            flows=flows, scheme_name=scheme_name, auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        authorization: str | None = request.cookies.get('Authorization')
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            return None

        return param


security = OAuth2PasswordBearerCookie(token_url='/login')  # noqa: S106


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Creates access token for user.

    Args:
        data: user data
        expires_delta: expire time for token

    Returns: token: str
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM,
    )


async def get_current_user(
    db_session: AsyncSession = Depends(get_session),
    token: str = Depends(security),
) -> User:
    """
    Get current user.

    Args:
        db_session: database async session
        token: jwt token

    Returns: User
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise credentials_exception from None

    username: str | None = payload.get('sub')
    if username is None:
        raise credentials_exception

    token_data: TokenData = TokenData(username=username)

    user = await get_user_by_username(
        db_session, token_data.username,
    )
    if not user:
        raise credentials_exception

    return user
