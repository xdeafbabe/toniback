import datetime

import async_asgi_testclient
import pytest
import pytz


@pytest.fixture
def existing_post() -> dict:
    return {
        'id': 1,
        'title': 'Title',
        'content': 'Content',
        'created_at': datetime.datetime(
            2010, 1, 1,
            0, 0, 0,
            tzinfo=pytz.UTC,
        ).isoformat(),
        'updated_at': None,
    }


@pytest.mark.asyncio
async def test_posts_get(
    api_client: async_asgi_testclient.TestClient,
    existing_post: dict,
):
    resp = await api_client.get('/posts/')
    assert resp.status_code == 200
    assert resp.json() == {'posts': [existing_post]}


@pytest.mark.asyncio
async def test_posts_get_by_id(
    api_client: async_asgi_testclient.TestClient,
    existing_post: dict,
):
    resp = await api_client.get(f'/posts/{existing_post["id"]}')
    assert resp.status_code == 200
    assert resp.json() == existing_post


@pytest.mark.asyncio
async def test_posts_get_by_id_nonexistent(
    api_client: async_asgi_testclient.TestClient,
):
    resp = await api_client.get('/posts/0')
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_posts_create(
    api_client: async_asgi_testclient.TestClient,
):
    new_post = {
        'title': 'New title',
        'content': 'New content',
    }

    resp = await api_client.post('/posts/', json=new_post)
    assert resp.status_code == 200
    created = resp.json()

    resp = await api_client.get(f'/posts/{created["id"]}')
    assert resp.status_code == 200
    fetched = resp.json()

    assert created == fetched


@pytest.mark.asyncio
async def test_posts_update(
    api_client: async_asgi_testclient.TestClient,
    existing_post: dict,
):
    updated_post = {
        'title': 'New title',
        'content': 'New content',
    }

    resp = await api_client.put(
        f'/posts/{existing_post["id"]}', json=updated_post)
    assert resp.status_code == 200
    updated = resp.json()

    assert updated['updated_at'] is not None

    resp = await api_client.get(f'/posts/{existing_post["id"]}')
    assert resp.status_code == 200
    fetched = resp.json()

    assert updated == fetched


@pytest.mark.asyncio
async def test_posts_update_nonexistent(
    api_client: async_asgi_testclient.TestClient,
):
    updated_post = {
        'title': 'New title',
        'content': 'New content',
    }

    resp = await api_client.put('/posts/0', json=updated_post)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_posts_delete(
    api_client: async_asgi_testclient.TestClient,
    existing_post: dict,
):
    resp = await api_client.delete(f'/posts/{existing_post["id"]}')
    assert resp.status_code == 200
    resp = await api_client.get(f'/posts/{existing_post["id"]}')
    assert resp.status_code == 404
