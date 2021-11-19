import sqlalchemy
import sqlalchemy.sql

from .. import schemas
from ..core import postgres


Blog = sqlalchemy.Table(
    'blog',
    postgres.metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column('description', sqlalchemy.Text, nullable=False),
)


class BlogDoesNotExist(Exception):
    """Raised on attempt to query nonexistent blog."""


async def blog_create(blog: schemas.BlogCreate) -> schemas.BlogGet:
    query = Blog.insert().values(**blog.dict()).returning(*Blog.c)
    created = await postgres.get_session().fetch_one(query)
    return schemas.BlogGet(**created)


async def blog_get_by_id(blog_id: int) -> schemas.BlogGet:
    query = Blog.select().where(Blog.c.id == blog_id)
    fetched = await postgres.get_session().fetch_one(query)

    if not fetched:
        raise BlogDoesNotExist

    return schemas.BlogGet(**fetched)


async def blog_get() -> schemas.BlogGetList:
    query = Blog.select()
    fetched = await postgres.get_session().fetch_all(query)
    return schemas.BlogGetList(blogs=fetched)


async def blog_update(
    blog_id: int,
    blog: schemas.BlogUpdate,
) -> schemas.BlogGet:
    query = Blog.update().where(
        Blog.c.id == blog_id,
    ).values(**blog.dict()).returning(*Blog.c)
    updated = await postgres.get_session().fetch_one(query)

    if not updated:
        raise BlogDoesNotExist

    return schemas.BlogGet(**updated)


async def blog_delete(blog_id: int) -> None:
    query = Blog.delete().where(Blog.c.id == blog_id)
    await postgres.get_session().execute(query)
