import datetime
import typing

import pydantic


class PostBase(pydantic.BaseModel):
    title: pydantic.constr(min_length=1, max_length=100)
    content: pydantic.constr(min_length=1)


class PostCreate(PostBase):
    pass


class PostGet(PostBase):
    id: int
    created_at: datetime.datetime
    updated_at: typing.Optional[datetime.datetime]


class PostGetList(pydantic.BaseModel):
    posts: list[PostGet]


class PostUpdate(PostBase):
    pass
