import async_asgi_testclient
import pytest


@pytest.fixture
def existing_blog() -> dict:
    return {
        'id': 1,
        'name': 'Name',
        'description': 'Description',
    }


@pytest.mark.asyncio
async def test_blogs_get(
    api_client: async_asgi_testclient.TestClient,
    existing_blog: dict,
):
    resp = await api_client.get('/blogs/')
    assert resp.status_code == 200
    assert resp.json() == {'blogs': [existing_blog]}


@pytest.mark.asyncio
async def test_blogs_get_by_id(
    api_client: async_asgi_testclient.TestClient,
    existing_blog: dict,
):
    resp = await api_client.get(f'/blogs/{existing_blog["id"]}')
    assert resp.status_code == 200
    assert resp.json() == existing_blog


@pytest.mark.asyncio
async def test_blogs_get_by_id_nonexistent(
    api_client: async_asgi_testclient.TestClient,
):
    resp = await api_client.get('/blogs/0')
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_blogs_create(
    api_client: async_asgi_testclient.TestClient,
):
    new_blog = {
        'name': 'New name',
        'description': 'New description',
    }

    resp = await api_client.post('/blogs/', json=new_blog)
    assert resp.status_code == 200
    created = resp.json()

    resp = await api_client.get(f'/blogs/{created["id"]}')
    assert resp.status_code == 200
    fetched = resp.json()

    assert created == fetched


@pytest.mark.asyncio
async def test_blogs_update(
    api_client: async_asgi_testclient.TestClient,
    existing_blog: dict,
):
    updated_blog = {
        'name': 'New name',
        'description': 'New description',
    }

    resp = await api_client.put(
        f'/blogs/{existing_blog["id"]}', json=updated_blog)
    assert resp.status_code == 200
    updated = resp.json()

    resp = await api_client.get(f'/blogs/{existing_blog["id"]}')
    assert resp.status_code == 200
    fetched = resp.json()

    assert updated == fetched


@pytest.mark.asyncio
async def test_blogs_update_nonexistent(
    api_client: async_asgi_testclient.TestClient,
):
    updated_blog = {
        'name': 'New name',
        'description': 'New description',
    }

    resp = await api_client.put('/blogs/0', json=updated_blog)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_blogs_delete(
    api_client: async_asgi_testclient.TestClient,
    existing_blog: dict,
):
    resp = await api_client.delete(f'/blogs/{existing_blog["id"]}')
    assert resp.status_code == 200
    resp = await api_client.get(f'/blogs/{existing_blog["id"]}')
    assert resp.status_code == 404
