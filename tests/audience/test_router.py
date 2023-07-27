from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.audience.router import get_router
from app.audience.schemas import (
    GetAudienceAggregationRequest,
    GetAudienceAggregationResponse,
    GetAudienceRequest,
    GetAudienceResponse,
)
from app.audience.service import AudienceService


@pytest.fixture
def audience_service():
    return AsyncMock(spec=AudienceService)


@pytest.fixture
def client_v1(audience_service):
    return TestClient(get_router(audience_service))


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/audience/foo",
            GetAudienceRequest(
                audience_name="foo",
            ),
        ),
        (
            "/v1/audience/foo?where_field=bar&where_values=biz,buzz&where_operator=contains&search=search_term&limit=9&offset=1",
            GetAudienceRequest(
                audience_name="foo",
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                search="search_term",
                limit=9,
                offset=1,
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_audience_v1(client_v1, audience_service, path, expected_request):
    # Setup the mock to return a specific value
    audience_service.get_audience.return_value = GetAudienceResponse(items=[], total=42)

    # Send a GET request to the /healthcheck endpoint
    response = client_v1.get(path)

    # Check the mock was called with the expected arguments
    audience_service.get_audience.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'items': [], 'total': 42}


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/audience/foo/aggregation?agg_type=count&agg_field=bar&where_field=bar&where_values=biz&where_operator=eq",
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count",
                agg_field="bar",
                where_field="bar",
                where_values=["biz"],
                where_operator="eq",
            ),
        ),
        (
            "/v1/audience/foo/aggregation?agg_type=count_bucket_values&agg_field=bar&where_field=bar&where_values=biz&where_operator=eq&buckets=1,2",
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count_bucket_values",
                agg_field="bar",
                where_field="bar",
                where_values=["biz"],
                where_operator="eq",
                buckets=['1', '2'],
            ),
        ),
        (
            "/v1/audience/foo/aggregation?agg_type=count_bucket_intervals&agg_field=bar&where_field=bar&where_values=biz&where_operator=eq&buckets=f:1;t:2",
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count_bucket_intervals",
                agg_field="bar",
                where_field="bar",
                where_values=["biz"],
                where_operator="eq",
                buckets=['f:1;t:2'],
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_audience_aggregation(
    client_v1, audience_service, path, expected_request
):
    # Setup the mock to return a specific value
    audience_service.get_aggregation.return_value = GetAudienceAggregationResponse(
        values=[42, 100]
    )

    # Send a GET request to the endpoint
    response = client_v1.get(path)

    # Check the mock was called with the expected arguments
    audience_service.get_aggregation.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {
        "values": [42, 100],
    }
