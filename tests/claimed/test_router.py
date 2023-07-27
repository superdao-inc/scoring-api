from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient


from app.claimed.schemas import (
    GetClaimedAggregationRequest,
    GetClaimedAggregationResponse,
    GetClaimedRequest,
    GetClaimedResponse,
)
from app.claimed.service import ClaimedService
from app.common.enums import BlockchainType
from app.claimed.router import get_router


@pytest.fixture
def claimed_service():
    return AsyncMock(ClaimedService)


@pytest.fixture
def client_v1(claimed_service):
    return TestClient(get_router(claimed_service))


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/claimed/0x1/polygon",
            GetClaimedRequest(
                claimed_contract="0x1",
                blockchain=BlockchainType.POLYGON,
            ),
        ),
        (
            "/v1/claimed/0x1?where_field=bar&where_values=biz,buzz&where_operator=contains&search=search_term&limit=9&offset=10",
            GetClaimedRequest(
                claimed_contract="0x1",
                blockchain=None,
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                search="search_term",
                limit=9,
                offset=10,
            ),
        ),
        (
            "/v1/claimed/0x1/eth?where_field=bar&where_values=biz,buzz&where_operator=contains&search=search_term&limit=9&offset=10",
            GetClaimedRequest(
                claimed_contract="0x1",
                blockchain=BlockchainType.ETHEREUM,
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
async def test_get_claimed_v1(client_v1, claimed_service, path, expected_request):
    # Setup the mock to return a specific value
    claimed_service.get_claimed.return_value = GetClaimedResponse(items=[], total=44)

    # Send a GET request to the endpoint
    response = client_v1.get(path)

    # Check the mock was called with the expected arguments
    claimed_service.get_claimed.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'items': [], 'total': 44}


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/claimed/0x1/aggregation/polygon?agg_type=count&agg_field=bar",
            GetClaimedAggregationRequest(
                claimed_contract="0x1",
                blockchain=BlockchainType.POLYGON,
                agg_type="count",
                agg_field="bar",
            ),
        ),
        (
            "/v1/claimed/0x1/aggregation/eth?agg_type=count_bucket_intervals&agg_field=bar&where_field=bar&where_values=biz,buzz&where_operator=contains&buckets=f:1;t:2",
            GetClaimedAggregationRequest(
                claimed_contract="0x1",
                blockchain=BlockchainType.ETHEREUM,
                agg_type="count_bucket_intervals",
                agg_field="bar",
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                buckets=["f:1;t:2"],
            ),
        ),
        (
            "/v1/claimed/0x1/aggregation?agg_type=count_bucket_values&&agg_field=bar&where_field=bar&where_values=biz,buzz&where_operator=contains&buckets=1,2",
            GetClaimedAggregationRequest(
                claimed_contract="0x1",
                blockchain=None,
                agg_type="count_bucket_values",
                agg_field="bar",
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                buckets=['1', '2'],
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_aggregation(client_v1, claimed_service, path, expected_request):
    # Setup the mock to return a specific value
    claimed_service.get_aggregation.return_value = GetClaimedAggregationResponse(
        values=[]
    )

    # Send a GET request to the endpoint
    response = client_v1.get(path)

    # Check the mock was called with the expected arguments
    claimed_service.get_aggregation.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'values': []}
