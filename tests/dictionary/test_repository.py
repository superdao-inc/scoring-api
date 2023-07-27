import pytest
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from app.dictionary.enums import DictionaryValueType

from app.dictionary.models import DictionaryItem
from app.dictionary.repository import DictionaryRepository


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
    return DictionaryRepository(session)


@pytest.fixture
def dictionary_objects():
    return [
        DictionaryItem(
            key='eth_price_usd',
            value='42',
            value_type=DictionaryValueType.INTEGER,
            updated=42,
        )
    ]


@pytest.mark.asyncio
async def test_fetch_dictionary(repository, dictionary_objects):
    repository.session.s.execute.return_value = MagicMock(
        one_or_none=MagicMock(return_value=dictionary_objects)
    )

    await repository.fetch_dictionary()

    # Check that the query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == str(
        sa.select(DictionaryItem)
        .select_from(DictionaryItem)
        .order_by(DictionaryItem.key)
        .compile(compile_kwargs={"literal_binds": True})
    )
