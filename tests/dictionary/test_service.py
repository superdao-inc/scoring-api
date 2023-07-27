import pytest
from unittest.mock import AsyncMock
from app.dictionary.enums import DictionaryValueType
from app.dictionary.models import DictionaryItem
from app.dictionary.schemas import GetDictionaryResponse

from app.dictionary.repository import DictionaryRepository
from app.dictionary.service import DictionaryService


@pytest.fixture
def dictionary_repository():
    return AsyncMock(spec=DictionaryRepository)


@pytest.fixture
def dictionary_service(dictionary_repository):
    return DictionaryService(dictionary_repository)


@pytest.mark.asyncio
async def test_fetch_dictionary(dictionary_repository, dictionary_service):
    # Arrange
    dictionary_repository.fetch_dictionary.return_value = [
        DictionaryItem(
            key='eth_price_usd',
            value='42',
            value_type=DictionaryValueType.INTEGER,
            updated=42,
        )
    ]

    # Act
    response = await dictionary_service.get_dictionary()

    # Assert
    dictionary_repository.fetch_dictionary.assert_called_once_with()
    assert isinstance(response, GetDictionaryResponse)
    assert response.eth_price_usd == 42


@pytest.mark.asyncio
async def test_fetch_dictionary_empty(dictionary_repository, dictionary_service):
    # Arrange
    dictionary_repository.fetch_dictionary.return_value = []

    # Act
    response = await dictionary_service.get_dictionary()

    # Assert
    dictionary_repository.fetch_dictionary.assert_called_once_with()
    assert response == GetDictionaryResponse()
