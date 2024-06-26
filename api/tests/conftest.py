import pytest

from typing import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import NullPool

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.auth.utils import create_access_token
from api.core import config
from api.core.database import Model, get_db
from api.main import app
from api.monitoring import crud as monitoring_crud
from api.monitoring.persistence import WebsiteMonitor
from api.monitoring.schemas import WebsiteMonitorCreate
from api.user import crud as user_crud
from api.user.persistence import User
from api.user.schemas import CreateUser

DATABASE_URL = f'postgresql+asyncpg://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:5432/webeye_test_db'
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
factory = async_sessionmaker(engine, autoflush=False, autocommit=False, expire_on_commit=False)


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    async with factory() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise


@pytest.fixture(scope='package')
def client():
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)
    yield


async def create_auth_user(name: str = 'test', email: str = 'test@test.com') -> tuple[User, str]:
    async with factory() as session:
        user = CreateUser(name=name, email=email, password='test12345')
        user = await user_crud.add(user, session)
        access_token = create_access_token(user.id, user.name)
        return user, access_token


async def enrich_user_with_monitoring(user: User) -> WebsiteMonitor:
    monitor_create = WebsiteMonitorCreate(url='https://test.com', interval_minutes=1)
    async with factory() as session:
        monitor = await monitoring_crud.add(monitor_create, user, session)
        return monitor