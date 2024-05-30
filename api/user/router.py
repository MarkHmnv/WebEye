from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import get_auth_user
from api.database import get_db
from api.user import crud
from api.user.persistence import User
from api.user.schemas import UserProfile, UpdateUserPartial

user_router = APIRouter(
    prefix='/users',
    tags=['Users API'],
)


@user_router.get('/profile', response_model=UserProfile)
def get_user_profile(user: User = Depends(get_auth_user)):
    return user


@user_router.patch('/profile', response_model=UserProfile)
async def update_user_profile(
        updated_user: UpdateUserPartial,
        user_to_update: User = Depends(get_auth_user),
        session: AsyncSession = Depends(get_db)
):
    return await crud.update_user(user_to_update, updated_user, session)


@user_router.delete('/profile', status_code=204)
async def delete_user(
        user_to_delete: User = Depends(get_auth_user),
        session: AsyncSession = Depends(get_db)
):
    await crud.delete(user_to_delete, session)