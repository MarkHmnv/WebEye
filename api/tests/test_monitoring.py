import pytest
from fastapi.testclient import TestClient

from api.monitoring import crud
from api.monitoring.schemas import WebsiteMonitorCreate, WebsiteMonitorResponse
from api.tests.conftest import create_auth_user, factory, enrich_user_with_monitoring


@pytest.mark.asyncio
async def test_create_monitoring_success(client: TestClient):
    user, access_token = await create_auth_user()
    monitor_create = WebsiteMonitorCreate(url='https://test.com', interval_minutes=1)
    response = client.post(
        '/api/v1/monitoring',
        json=monitor_create.model_dump(),
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 201
    async with factory() as session:
        assert await crud.exists_by_url(monitor_create.url, user.id, session)
    assert response.json()['url'] == monitor_create.url


@pytest.mark.asyncio
async def test_create_monitoring_already_exists(client: TestClient):
    user, access_token = await create_auth_user()
    await enrich_user_with_monitoring(user)
    monitor_create = WebsiteMonitorCreate(url='https://test.com', interval_minutes=1)
    response = client.post(
        '/api/v1/monitoring',
        json=monitor_create.model_dump(),
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 409


def test_create_monitoring_unauthorized(client: TestClient):
    monitor_create = WebsiteMonitorCreate(url='https://test.com', interval_minutes=1)
    response = client.post('/api/v1/monitoring', json=monitor_create.model_dump())
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_monitors_success(client: TestClient):
    user, access_token = await create_auth_user()
    monitor = await enrich_user_with_monitoring(user)
    monitor_response = WebsiteMonitorResponse.model_validate(monitor, from_attributes=True)
    response = client.get('/api/v1/monitoring', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json() == [monitor_response.model_dump()]


def test_get_all_monitors_unauthorized(client: TestClient):
    response = client.get('/api/v1/monitoring')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_monitor_success(client: TestClient):
    user, access_token = await create_auth_user()
    monitor = await enrich_user_with_monitoring(user)
    response = client.delete(f'/api/v1/monitoring/{monitor.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204
    async with factory() as session:
        assert not await crud.exists_by_url(monitor.url, user.id, session)


def test_delete_monitor_unauthorized(client: TestClient):
    response = client.delete('/api/v1/monitoring/1')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_another_user_monitor(client: TestClient):
    user, access_token = await create_auth_user()
    another_user, _ = await create_auth_user(name='test2', email='test2@test.com')
    monitor = await enrich_user_with_monitoring(another_user)
    response = client.delete(f'/api/v1/monitoring/{monitor.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
