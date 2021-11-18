import uuid

import pytest
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy_utils

import toniback.core.config
import toniback.core.postgres
import toniback.models


@pytest.fixture(autouse=True)
def prepare_test_database():
    database = f'toni_test_{uuid.uuid4()}'
    toniback.core.config.postgres.database = database
    url = sqlalchemy.engine.make_url(toniback.core.config.postgres.url)
    engine = sqlalchemy.create_engine(url)
    sqlalchemy_utils.create_database(engine.url)
    toniback.core.postgres.metadata.create_all(engine)
    yield
    sqlalchemy_utils.drop_database(engine.url)
