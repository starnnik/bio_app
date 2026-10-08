from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.api.v1.dependencies import CurrentUser, SessionDep
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.schemas.user import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: SessionDep) -> User:
    if await session.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    return user


@router.post("/login", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = await session.scalar(select(User).where(User.email == form.username))
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserRead)
async def me(user: CurrentUser) -> User:
    return user
