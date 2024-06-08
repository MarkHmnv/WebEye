import pytest
from fastapi.testclient import TestClient

from api.tests.conftest import factory, create_auth_user
from api.user import crud
from api.user.schemas import UserProfile, UpdateUserPartial


@pytest.mark.asyncio
async def test_get_user_profile_success(client: TestClient):
    user, access_token = await create_auth_user()
    user_profile = UserProfile.model_validate(user, from_attributes=True)
    response = client.get('/api/v1/users/profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json() == user_profile.model_dump()


def test_get_user_profile_unauthorized(client: TestClient):
    response = client.get('/api/v1/users/profile')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_user_profile_success(client: TestClient):
    user, access_token = await create_auth_user()
    update_user = UpdateUserPartial(name='test2')
    response = client.patch(
        '/api/v1/users/profile',
        json=update_user.model_dump(),
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 200
    assert response.json()['name'] == update_user.name


def test_update_user_profile_unauthorized(client: TestClient):
    update_user = UpdateUserPartial(name='test2')
    response = client.patch('/api/v1/users/profile', json=update_user.model_dump())
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_profile_success(client: TestClient):
    user, access_token = await create_auth_user()
    response = client.delete('/api/v1/users/profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204
    async with factory() as session:
        assert not await crud.exists_by_email(user.email, session)


def test_delete_user_profile_unauthorized(client: TestClient):
    response = client.delete('/api/v1/users/profile')
    assert response.status_code == 401