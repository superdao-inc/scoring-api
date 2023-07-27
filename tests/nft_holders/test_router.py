from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.nft_holders.schemas import (
    GetNftHoldersRequest,
    GetNftHoldersResponse,
)
from app.nft_holders.service import NftHoldersService
from app.nft_holders.router import get_router


@pytest.fixture
def nft_holders_service():
    return AsyncMock(NftHoldersService)


@pytest.fixture
def client(nft_holders_service):
    return TestClient(get_router(nft_holders_service))


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/nft_holders/0x1",
            GetNftHoldersRequest(
                collection_address="0x1",
            ),
        ),
        (
            "/v1/nft_holders/0x1?where_field=bar&where_values=biz,buzz&where_operator=contains&search=search_term&limit=9&offset=10",
            GetNftHoldersRequest(
                collection_address="0x1",
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                search="search_term",
                limit=9,
                offset=10,
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_nft_holders(client, nft_holders_service, path, expected_request):
    # Setup the mock to return a specific value
    nft_holders_service.get_nft_holders_scrolled.return_value = GetNftHoldersResponse(
        items=[], has_more=True
    )

    # Send a GET request to the endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    nft_holders_service.get_nft_holders_scrolled.assert_called_once_with(
        expected_request
    )

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'items': [], 'has_more': True}
