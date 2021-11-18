import datetime

import pytz
import sqlalchemy
import sqlalchemy.sql

from .. import schemas
from ..core import postgres


Post = sqlalchemy.Table(
    'post',
    postgres.metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column('content', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(
        'created_at',
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy.sql.text('NOW()'),
        index=True,
    ),
    sqlalchemy.Column(
        'updated_at',
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
    ),
)


class PostDoesNotExist(Exception):
    """Raised on attempt to query nonexistent post."""


async def post_create(post: schemas.PostCreate) -> schemas.PostGet:
    query = Post.insert().values(**post.dict()).returning(*Post.c)
    created = await postgres.get_session().fetch_one(query)
    return schemas.PostGet(**created)


async def post_get_by_id(post_id: int) -> schemas.PostGet:
    query = Post.select().where(Post.c.id == post_id)
    fetched = await postgres.get_session().fetch_one(query)

    if not fetched:
        raise PostDoesNotExist

    return schemas.PostGet(**fetched)


async def post_get() -> schemas.PostGetList:
    query = Post.select()
    fetched = await postgres.get_session().fetch_all(query)
    return schemas.PostGetList(posts=fetched)


async def post_update(
    post_id: int,
    post: schemas.PostUpdate,
) -> schemas.PostGet:
    query = Post.update().where(
        Post.c.id == post_id,
    ).values(
        **post.dict(),
        updated_at=datetime.datetime.now(tz=pytz.UTC),
    ).returning(*Post.c)
    updated = await postgres.get_session().fetch_one(query)

    if not updated:
        raise PostDoesNotExist

    return schemas.PostGet(**updated)


async def post_delete(post_id: int) -> None:
    query = Post.delete().where(Post.c.id == post_id)
    await postgres.get_session().execute(query)
