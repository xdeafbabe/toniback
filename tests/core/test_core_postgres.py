import databases
import pytest

import toniback.core.postgres


@pytest.mark.asyncio
async def test_session():
    with pytest.raises(toniback.core.postgres.PostgresNotConnectedError):
        toniback.core.postgres.get_session()

    await toniback.core.postgres.connect()
    session = toniback.core.postgres.get_session()
    assert isinstance(session, databases.Database)
    await toniback.core.postgres.disconnect()

    with pytest.raises(toniback.core.postgres.PostgresNotConnectedError):
        toniback.core.postgres.get_session()
