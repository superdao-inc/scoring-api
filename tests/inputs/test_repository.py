import pytest
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa

from app.inputs.models import ActivityMetadata
from app.inputs.repository import ActivityMetadataRepository
from app.common.enums import BlockchainType


@pytest.fixture()
def session():
    class AsyncMockSessionMaker:
        s = AsyncMock()

        async def __aenter__(self, *args, **kwargs):
            return self.s

        async def __aexit__(self, *args, **kwargs):
            pass

    return AsyncMockSessionMaker


@pytest.fixture()
def repository(session):
    return ActivityMetadataRepository(session)


@pytest.fixture
def activity_metadata_objects():
    return [
        ActivityMetadata(
            address='0xA',
            chain=BlockchainType.ETHEREUM,
            name='A',
            external_url='external_url',
            image_url='image_url',
        )
    ]


@pytest.mark.asyncio
async def test_fetch_activity_metadatas(repository, activity_metadata_objects):
    repository.session.s.execute.return_value = MagicMock(
        one_or_none=MagicMock(return_value=activity_metadata_objects)
    )

    await repository.fetch_activity_metadatas()

    # Check that the query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == str(
        sa.select(ActivityMetadata)
        .select_from(ActivityMetadata)
        .order_by(ActivityMetadata.address)
        .compile(compile_kwargs={"literal_binds": True})
    )
