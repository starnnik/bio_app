from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import decode_access_token
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> User:
    user_id = decode_access_token(token)
    user = await session.get(User, user_id) if user_id is not None else None
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(user: CurrentUser) -> User:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin only")
    return user


AdminUser = Annotated[User, Depends(require_admin)]
