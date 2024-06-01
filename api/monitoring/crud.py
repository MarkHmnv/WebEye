from datetime import timedelta

from redbeat import RedBeatSchedulerEntry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.monitoring.persistence import WebsiteMonitor
from api.monitoring.schemas import WebsiteMonitorCreate
from api.core.celery_config import celery_app
from api.core.constants import WEBSITE_KEY
from api.core.redis_config import rd
from api.user.persistence import User


async def add(monitoring: WebsiteMonitorCreate, user: User, session: AsyncSession) -> WebsiteMonitor:
    monitor = WebsiteMonitor(**monitoring.dict(), user_id=user.id)
    session.add(monitor)
    await session.flush()
    await session.commit()
    return monitor


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


async def find_all_by_user_id(user_id: int, session: AsyncSession) -> list[WebsiteMonitor]:
    query = select(WebsiteMonitor).where(WebsiteMonitor.user_id == user_id)
    return list((await session.execute(query)).scalars().all())


def add_monitoring_to_scheduler(website_monitor: WebsiteMonitor):
    RedBeatSchedulerEntry(
        name=f'monitor_{website_monitor.id}_{website_monitor.user_id}',
        task='api.monitoring.tasks.monitor_website',
        args=[website_monitor.url, website_monitor.id, website_monitor.user_id],
        schedule=timedelta(seconds=website_monitor.interval_minutes),
        app=celery_app
    ).save()


def delete_monitoring_from_scheduler(website_monitor: WebsiteMonitor):
    RedBeatSchedulerEntry.from_key(
        key=f'redbeat:monitor_{website_monitor.id}_{website_monitor.user_id}',
        app=celery_app
    ).delete()
    rd.hdel(WEBSITE_KEY, f'{website_monitor.id}_{website_monitor.user_id}')