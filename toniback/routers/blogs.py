import fastapi

from .. import models
from .. import schemas


router = fastapi.APIRouter()


@router.get(
    '/',
    response_model=schemas.BlogGetList,
)
async def blogs_get():
    return await models.blog_get()


@router.get(
    '/{blog_id}',
    response_model=schemas.BlogGet,
)
async def blogs_get_by_id(blog_id: int):
    try:
        return await models.blog_get_by_id(blog_id)
    except models.BlogDoesNotExist:
        raise fastapi.HTTPException(status_code=404, detail='Blog not found')


@router.post(
    '/',
    response_model=schemas.BlogGet,
)
async def blogs_create(blog: schemas.BlogCreate):
    return await models.blog_create(blog)


@router.put(
    '/{blog_id}',
    response_model=schemas.BlogGet,
)
async def blogs_update(blog_id: int, blog: schemas.BlogUpdate):
    try:
        return await models.blog_update(blog_id, blog)
    except models.BlogDoesNotExist:
        raise fastapi.HTTPException(status_code=404, detail='Blog not found')


@router.delete('/{blog_id}')
async def blogs_delete(blog_id: int):
    await models.blog_delete(blog_id)
