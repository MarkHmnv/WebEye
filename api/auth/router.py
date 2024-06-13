import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import get_user_from_refresh_token
from api.auth.schemas import TokenResponse
from api.auth.utils import create_access_token, create_refresh_token
from api.core.database import get_db
from api.user import crud
from api.user.persistence import User
from api.user.schemas import CreateUser, LoginUser

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth API'],
)


@auth_router.post('/register', response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user: CreateUser, session: AsyncSession = Depends(get_db)):
    if await crud.exists_by_email(user.email, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='The user with this email already exists',
        )
    user = await crud.add(user, session)
    access_token = create_access_token(user.id, user.name)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post('/login', response_model=TokenResponse)
async def login(login_user: LoginUser, session: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(login_user.email, session)
    if user is None or not bcrypt.checkpw(login_user.password.encode(), user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    access_token = create_access_token(user.id, user.name)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post('/refresh', response_model=TokenResponse)
async def refresh(user: User = Depends(get_user_from_refresh_token)):
    access_token = create_access_token(user.id, user.name)
    refresh_token = create_refresh_token(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)