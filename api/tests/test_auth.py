import pytest
from pydantic import ValidationError

from api.auth.utils import create_refresh_token
from api.user import crud
from api.user.schemas import CreateUser, LoginUser

from fastapi.testclient import TestClient

from api.tests.conftest import factory


@pytest.mark.asyncio
async def test_register_success(client: TestClient):
    create_user = CreateUser(name='test', email='test@test.com', password='test12345')
    response = client.post('api/v1/auth/register', json=create_user.model_dump())
    assert response.status_code == 201
    async with factory() as session:
        assert await crud.exists_by_email(create_user.email, session)
    response = response.json()
    assert response['access_token']
    assert response['refresh_token']


@pytest.mark.asyncio
async def test_register_already_exists(client: TestClient):
    create_user = CreateUser(name='test', email='test@test.com', password='test12345')
    response = client.post('api/v1/auth/register', json=create_user.model_dump())
    assert response.status_code == 201
    response = client.post('api/v1/auth/register', json=create_user.model_dump())
    assert response.status_code == 409


def test_register_invalid_field(client: TestClient):
    try:
        CreateUser(name='test', email='test@test.com', password='short')
    except ValidationError as e:
        assert e


def test_login_success(client: TestClient):
    create_user = CreateUser(name='test', email='test@test.com', password='test12345')
    client.post('api/v1/auth/register', json=create_user.model_dump())
    login_user = LoginUser(email=create_user.email, password=create_user.password)
    response = client.post('api/v1/auth/login', json=login_user.model_dump())
    assert response.status_code == 200
    response = response.json()
    assert response['access_token']
    assert response['refresh_token']


def test_login_invalid_password(client: TestClient):
    create_user = CreateUser(name='test', email='test@test.com', password='test12345')
    client.post('api/v1/auth/register', json=create_user.model_dump())
    login_user = LoginUser(email=create_user.email, password='invalid_password')
    response = client.post('api/v1/auth/login', json=login_user.model_dump())
    assert response.status_code == 401


def test_login_user_not_exists(client: TestClient):
    login_user = LoginUser(email='test@test.com', password='test12345')
    response = client.post('api/v1/auth/login', json=login_user.model_dump())
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_success(client: TestClient):
    create_user = CreateUser(name='test', email='test@test.com', password='test12345')
    response = client.post('api/v1/auth/register', json=create_user.model_dump())
    refresh_token = response.json()['refresh_token']

    response = client.post('api/v1/auth/refresh', json={"refresh_token": refresh_token})
    assert response.status_code == 200
    new_tokens = response.json()
    assert new_tokens['access_token']
    assert new_tokens['refresh_token']


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: TestClient):
    response = client.post('api/v1/auth/refresh', json={"refresh_token": "invalidtoken"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_expired(client: TestClient):
    create_user = CreateUser(name='test', email='test@test.com', password='test12345')
    client.post('api/v1/auth/register', json=create_user.model_dump())

    refresh_token = create_refresh_token(user_id=1, expire_days=-1)
    response = client.post('api/v1/auth/refresh', json={"refresh_token": refresh_token})
    assert response.status_code == 401