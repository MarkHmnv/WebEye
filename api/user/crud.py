import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.persistence import User
from api.user.schemas import CreateUser, UpdateUserPartial

import api.monitoring.crud as monitoring_crud


async def add(user: CreateUser, session: AsyncSession) -> User:
    dump = user.model_dump()
    password = dump.pop('password')
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(**dump, password=password)
    session.add(user)
    await session.flush()
    await session.commit()
    return user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    query = select(User).where(User.email == email)
    return (await session.execute(query)).scalar()


async def exists_by_email(email: str, session: AsyncSession) -> bool:
    query = select(User).where(User.email == email)
    return (await session.execute(query)).scalar() is not None


async def update_user(
        user_to_update: User,
        updated_user: UpdateUserPartial,
        session: AsyncSession
) -> User:
    for name, value in updated_user.model_dump(exclude_none=True).items():
        setattr(user_to_update, name, value)
    await session.flush()
    await session.commit()
    return user_to_update


async def delete(user_to_delete: User, session: AsyncSession):
    monitors = await monitoring_crud.find_all_by_user_id(user_to_delete.id, session)
    for monitor in monitors:
        monitoring_crud.delete_monitoring_from_scheduler(monitor)
    await session.delete(user_to_delete)
    await session.flush()
    await session.commit()
