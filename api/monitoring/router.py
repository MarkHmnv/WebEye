from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import get_auth_user
from api.core.database import get_db
from api.monitoring import crud
from api.monitoring.schemas import WebsiteMonitorCreate, WebsiteMonitorResponse
from api.user.persistence import User

monitoring_router = APIRouter(
    prefix='/monitoring',
    tags=['Monitoring API'],
)


@monitoring_router.post('', response_model=WebsiteMonitorResponse, status_code=status.HTTP_201_CREATED)
async def create_monitoring(
        monitoring: WebsiteMonitorCreate,
        auth_user: User = Depends(get_auth_user),
        session: AsyncSession = Depends(get_db)
):
    if await crud.exists_by_url(monitoring.url, auth_user.id, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='This website is already monitored by you',
        )
    website_monitor = await crud.add(monitoring, auth_user, session)
    crud.add_monitoring_to_scheduler(website_monitor)
    return website_monitor


@monitoring_router.get('', response_model=list[WebsiteMonitorResponse])
async def get_all_monitors(auth_user: User = Depends(get_auth_user),
                           session: AsyncSession = Depends(get_db)):
    return await crud.find_all_for_user(auth_user, session)


@monitoring_router.delete('/{monitoring_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_monitoring(
        monitoring_id: int,
        auth_user: User = Depends(get_auth_user),
        session: AsyncSession = Depends(get_db)
):
    website_monitor = await crud.get_by_id(monitoring_id, session)
    if website_monitor is None or website_monitor.user_id != auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You do not monitor this website',
        )
    await crud.delete(website_monitor, session)
    crud.delete_monitoring_from_scheduler(website_monitor)
