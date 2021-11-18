import datetime

import pytest
import pytz

import toniback.models
import toniback.schemas


@pytest.fixture
def existing_post() -> toniback.schemas.PostGet:
    return toniback.schemas.PostGet(
        id=1,
        title='Title',
        content='Content',
        created_at=datetime.datetime(
            2010, 1, 1,
            0, 0, 0,
            tzinfo=pytz.UTC,
        ),
        updated_at=None,
    )


@pytest.mark.asyncio
async def test_post_create(postgres: None):
    post_schema = toniback.schemas.PostCreate(
        title='Post title',
        content='Post content',
    )

    created = await toniback.models.post_create(post_schema)
    assert isinstance(created, toniback.schemas.PostGet)
    assert isinstance(created.id, int)
    assert isinstance(created.created_at, datetime.datetime)
    assert created.updated_at is None


@pytest.mark.asyncio
async def test_post_get_by_id(
    postgres: None,
    existing_post: toniback.schemas.PostGet,
):
    fetched = await toniback.models.post_get_by_id(existing_post.id)
    assert fetched == existing_post


@pytest.mark.asyncio
async def test_post_get_by_id_nonexistent(postgres: None):
    with pytest.raises(toniback.models.PostDoesNotExist):
        await toniback.models.post_get_by_id(0)


@pytest.mark.asyncio
async def test_post_get(
    postgres: None,
    existing_post: toniback.schemas.PostGet,
):
    fetched = await toniback.models.post_get()
    assert fetched.posts == [existing_post]


@pytest.mark.asyncio
@pytest.mark.freeze_time('2020-01-01 00:00:00+00')
async def test_post_update(
    postgres: None,
    existing_post: toniback.schemas.PostGet,
):
    title = 'Updated title'
    content = 'Updated content'

    update_schema = toniback.schemas.PostUpdate(
        title=title, content=content)

    updated = await toniback.models.post_update(1, update_schema)
    assert updated.id == existing_post.id
    assert updated.title == title
    assert updated.content == content
    assert updated.created_at == existing_post.created_at
    assert updated.updated_at == datetime.datetime.now(tz=pytz.UTC)


@pytest.mark.asyncio
async def test_post_update_nonexistent(postgres: None):
    update_schema = toniback.schemas.PostUpdate(title='New', content='New')

    with pytest.raises(toniback.models.PostDoesNotExist):
        await toniback.models.post_update(0, update_schema)


@pytest.mark.asyncio
async def test_post_delete(
    postgres: None,
    existing_post: toniback.schemas.PostGet,
):
    await toniback.models.post_delete(existing_post.id)

    with pytest.raises(toniback.models.PostDoesNotExist):
        await toniback.models.post_get_by_id(existing_post.id)

    all_posts = await toniback.models.post_get()
    assert all_posts.posts == []


@pytest.mark.asyncio
async def test_post_delete_nonexistent(postgres: None):
    await toniback.models.post_delete(0)
