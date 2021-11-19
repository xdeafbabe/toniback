import pytest

import toniback.models
import toniback.schemas


@pytest.fixture
def existing_blog() -> toniback.schemas.BlogGet:
    return toniback.schemas.BlogGet(
        id=1,
        name='Name',
        description='Description',
    )


@pytest.mark.asyncio
async def test_blog_create(postgres: None):
    blog_schema = toniback.schemas.BlogCreate(
        name='Blog name',
        description='Blog description',
    )

    created = await toniback.models.blog_create(blog_schema)
    assert isinstance(created, toniback.schemas.BlogGet)
    assert isinstance(created.id, int)


@pytest.mark.asyncio
async def test_blog_get_by_id(
    postgres: None,
    existing_blog: toniback.schemas.BlogGet,
):
    fetched = await toniback.models.blog_get_by_id(existing_blog.id)
    assert fetched == existing_blog


@pytest.mark.asyncio
async def test_blog_get_by_id_nonexistent(postgres: None):
    with pytest.raises(toniback.models.BlogDoesNotExist):
        await toniback.models.blog_get_by_id(0)


@pytest.mark.asyncio
async def test_blog_get(
    postgres: None,
    existing_blog: toniback.schemas.BlogGet,
):
    fetched = await toniback.models.blog_get()
    assert fetched.blogs == [existing_blog]


@pytest.mark.asyncio
@pytest.mark.freeze_time('2020-01-01 00:00:00+00')
async def test_blog_update(
    postgres: None,
    existing_blog: toniback.schemas.BlogGet,
):
    name = 'Updated name'
    description = 'Updated description'

    update_schema = toniback.schemas.BlogUpdate(
        name=name, description=description)

    updated = await toniback.models.blog_update(1, update_schema)
    assert updated.id == existing_blog.id
    assert updated.name == name
    assert updated.description == description


@pytest.mark.asyncio
async def test_blog_update_nonexistent(postgres: None):
    update_schema = toniback.schemas.BlogUpdate(name='New', description='New')

    with pytest.raises(toniback.models.BlogDoesNotExist):
        await toniback.models.blog_update(0, update_schema)


@pytest.mark.asyncio
async def test_blog_delete(
    postgres: None,
    existing_blog: toniback.schemas.BlogGet,
):
    await toniback.models.blog_delete(existing_blog.id)

    with pytest.raises(toniback.models.BlogDoesNotExist):
        await toniback.models.blog_get_by_id(existing_blog.id)

    all_blogs = await toniback.models.blog_get()
    assert all_blogs.blogs == []


@pytest.mark.asyncio
async def test_blog_delete_nonexistent(postgres: None):
    await toniback.models.blog_delete(0)
