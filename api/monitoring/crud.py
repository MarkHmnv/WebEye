from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.monitoring.persistence import WebsiteMonitor
from api.monitoring.schemas import WebsiteMonitorCreate
from api.user.persistence import User


async def add(monitoring: WebsiteMonitorCreate, user: User, session: AsyncSession):
    monitor = WebsiteMonitor(**monitoring.dict(), user_id=user.id)
    session.add(monitor)
    await session.flush()
    await session.commit()


async def find_all_for_user(user: User, session: AsyncSession) -> list[WebsiteMonitor]:
    query = select(WebsiteMonitor).where(WebsiteMonitor.user_id == user.id)
    return list((await session.execute(query)).scalars().all())


async def exists_by_url(url: str, user_id: int, session: AsyncSession) -> bool:
    query = select(WebsiteMonitor).where(
        WebsiteMonitor.url == url,
        WebsiteMonitor.user_id == user_id
    )
    return (await session.execute(query)).scalar() is not None


async def delete(website_monitor: WebsiteMonitor, session):
    await session.delete(website_monitor)
    await session.flush()
    await session.commit()


async def get_by_id(monitoring_id: int, session: AsyncSession) -> WebsiteMonitor | None:
    query = select(WebsiteMonitor).where(WebsiteMonitor.id == monitoring_id)
    return (await session.execute(query)).scalar()
