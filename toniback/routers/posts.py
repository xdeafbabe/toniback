import fastapi

from .. import models
from .. import schemas


router = fastapi.APIRouter()


@router.get(
    '/',
    response_model=schemas.PostGetList,
)
async def posts_get():
    return await models.post_get()


@router.get(
    '/{post_id}',
    response_model=schemas.PostGet,
)
async def posts_get_by_id(post_id: int):
    try:
        return await models.post_get_by_id(post_id)
    except models.PostDoesNotExist:
        raise fastapi.HTTPException(status_code=404, detail='Post not found')


@router.post(
    '/',
    response_model=schemas.PostGet,
)
async def posts_create(post: schemas.PostCreate):
    return await models.post_create(post)


@router.put(
    '/{post_id}',
    response_model=schemas.PostGet,
)
async def posts_update(post_id: int, post: schemas.PostUpdate):
    try:
        return await models.post_update(post_id, post)
    except models.PostDoesNotExist:
        raise fastapi.HTTPException(status_code=404, detail='Post not found')


@router.delete('/{post_id}')
async def posts_delete(post_id: int):
    await models.post_delete(post_id)
