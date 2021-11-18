import typing

import databases
import sqlalchemy

from . import config


class PostgresNotConnectedError(Exception):
    """Raised on attempt to get nonexistent PostgreSQL session."""


metadata = sqlalchemy.MetaData()
session = typing.Optional[databases.Database]


async def connect() -> None:
    global session

    if not session:
        session = databases.Database(config.postgres.url)
        await session.connect()


async def disconnect() -> None:
    global session

    if session:
        await session.disconnect()
        session = None


def get_session() -> databases.Database:
    global session

    if not session:
        raise PostgresNotConnectedError

    return session
