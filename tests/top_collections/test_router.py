import pytest
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from app.common.enums import AudienceType, BlockchainType

from app.top_collections.service import TopCollectionsService
from app.top_collections.router import get_router
from app.top_collections.schemas import (
    TopCollectionsQuery,
    TopCollectionsResponse,
    TopCollectionsItem,
)


@pytest.fixture
def service():
    return AsyncMock(spec=TopCollectionsService)


@pytest.fixture
def client(service):
    return TestClient(get_router(service))


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/top-collections?top_n=15&audience_id=foo&audience_type=claimed&blockchain=eth",
            TopCollectionsQuery(
                audience_id='foo',
                audience_type=AudienceType.CLAIMED,
                top_n=15,
                blockchain=BlockchainType.ETHEREUM,
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_router(client, service, path, expected_request):
    service.get_top_collections.return_value = TopCollectionsResponse(
        items=[
            TopCollectionsItem(
                audience_id="foo",
                audience_type=AudienceType.CLAIMED,
                blockchain=BlockchainType.ETHEREUM,
                contract_address="0x1234",
                nfts_count=1,
                holders_count=0,
                total_nfts_count=0,
                total_holders_count=0,
                updated=100,
            )
        ]
    )

    response = client.get(path)

    service.get_top_collections.assert_called_once_with(expected_request)

    assert response.status_code == 200

    assert response.json() == {
        "items": [
            {
                "audience_id": "foo",
                "audience_type": AudienceType.CLAIMED.value,
                "blockchain": BlockchainType.ETHEREUM.value,
                "contract_address": "0x1234",
                "nfts_count": 1,
                "holders_count": 0,
                "total_nfts_count": 0,
                "total_holders_count": 0,
                "updated": 100,
            }
        ]
    }
