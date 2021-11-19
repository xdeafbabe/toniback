import pydantic


class BlogBase(pydantic.BaseModel):
    name: pydantic.constr(min_length=1, max_length=100)
    description: pydantic.constr(min_length=1, max_length=4000)


class BlogCreate(BlogBase):
    pass


class BlogGet(BlogBase):
    id: int


class BlogGetList(pydantic.BaseModel):
    blogs: list[BlogGet]


class BlogUpdate(BlogBase):
    pass
