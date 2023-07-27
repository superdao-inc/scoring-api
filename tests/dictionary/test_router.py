from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.dictionary.service import DictionaryService
from app.dictionary.router import get_router
from app.dictionary.schemas import GetDictionaryResponse


@pytest.fixture
def dictionary_service():
    return AsyncMock(spec=DictionaryService)


@pytest.fixture
def client(dictionary_service):
    return TestClient(get_router(dictionary_service))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path, service_return_value, expected_json",
    [
        (
            "/v1/dictionary",
            GetDictionaryResponse(
                eth_price_usd=42,
                last_block_timestamp=1600000042,
            ),
            {
                'eth_price_usd': 42,
                'last_block_timestamp': 1600000042,
            },
        ),
        (
            "/v1/dictionary",
            GetDictionaryResponse(),
            {
                'eth_price_usd': None,
                'last_block_timestamp': None,
            },
        ),
    ],
)
async def test_get(
    client, dictionary_service, path, service_return_value, expected_json
):
    # Setup the mock to return a specific value
    dictionary_service.get_dictionary.return_value = service_return_value

    # Send a GET request to the /dictionary endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    dictionary_service.get_dictionary.assert_called_once_with()

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == expected_json
