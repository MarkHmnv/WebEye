import os
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr

POSTGRES_USER = os.getenv('POSTGRES_USER', 'devuser')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'changeme')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'devdb')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
engine = create_async_engine(DATABASE_URL, echo=True)
factory = async_sessionmaker(engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Model(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with factory() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
