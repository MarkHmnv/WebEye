import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.schemas import TokenResponse
from api.auth.utils import encode_jwt
from api.database import get_db
from api.user import crud
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
    payload = dict(sub=user.id, name=user.name)
    return TokenResponse(access_token=encode_jwt(payload))


@auth_router.post('/login', response_model=TokenResponse)
async def login(login_user: LoginUser, session: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(login_user.email, session)
    if user is None or not bcrypt.checkpw(login_user.password.encode(), user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    payload = dict(sub=user.id, name=user.name)
    return TokenResponse(access_token=encode_jwt(payload))