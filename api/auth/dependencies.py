from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.utils import decode_jwt
from api.core.database import get_db
from api.user import crud
from api.user.persistence import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login'
)


def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_jwt(token)
    exp = payload.get('exp', 0)
    if datetime.utcnow() > datetime.fromtimestamp(exp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token',
        )
    return payload


async def get_auth_user(
        token_payload: dict = Depends(get_token_payload),
        session: AsyncSession = Depends(get_db)
) -> User:
    user_id = token_payload.get('sub', -1)
    user = await crud.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token',
        )
    return user
