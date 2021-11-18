import uuid

import databases
import pytest
import pytest_mock
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy_utils

import toniback.core.config
import toniback.core.postgres
import toniback.models


@pytest.fixture(autouse=True, scope='session')
def prepare_test_database() -> None:
    database = f'toni_test_{uuid.uuid4()}'
    toniback.core.config.postgres.database = database
    url = sqlalchemy.engine.make_url(toniback.core.config.postgres.url)
    engine = sqlalchemy.create_engine(url)
    sqlalchemy_utils.create_database(engine.url)
    toniback.core.postgres.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text("""
            INSERT INTO post (title, content, created_at)
            VALUES ('Title', 'Content', '2010-01-01 00:00:00+00');
        """))
    yield
    sqlalchemy_utils.drop_database(engine.url)


@pytest.fixture()
async def postgres(mocker: pytest_mock.MockerFixture) -> None:
    session = databases.Database(
        toniback.core.config.postgres.url,
        force_rollback=True,
    )
    await session.connect()
    mocker.patch('toniback.core.postgres.get_session', return_value=session)
    yield
    await session.disconnect()
