from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.analytics.router import get_router
from app.analytics.schemas import (
    ConversionPoint,
    GetAggregationsRequest,
    GetAggregationsResponse,
    GetAnalyticsRequest,
    GetAnalyticsResponse,
    GetConversionsRequest,
    GetConversionsResponse,
    GetEventsStatsRequest,
    GetEventsStatsResponse,
    EventBucket,
    SourceBucket,
)
from app.analytics.service import AnalyticsService


@pytest.fixture
def analytics_service():
    return AsyncMock(spec=AnalyticsService)


@pytest.fixture
def client(analytics_service):
    return TestClient(get_router(analytics_service))


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/analytics/foo",
            GetAnalyticsRequest(
                tracker_id="foo",
            ),
        ),
        (
            "/v1/analytics/foo?order_by_field=score&order_by_direction=DESC&where_field=labels&where_operator=contains&where_values=whale,shark&search=some_search_string&limit=100&offset=200",
            GetAnalyticsRequest(
                tracker_id="foo",
                order_by_field="score",
                order_by_direction="DESC",
                where_field="labels",
                where_operator="contains",
                where_values=["whale", "shark"],
                search="some_search_string",
                limit=100,
                offset=200,
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_analytics(client, analytics_service, path, expected_request):
    # Setup the mock to return a specific value
    analytics_service.get_analytics.return_value = GetAnalyticsResponse(
        items=[], total=14
    )

    # Create a TestClient instance
    client = TestClient(get_router(analytics_service))

    # Send a GET request to the /analytics/:tracker_id endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    analytics_service.get_analytics.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'items': [], 'total': 14}


@pytest.mark.asyncio
async def test_get_analytics_aggregations(analytics_service):
    # Setup the mock to return a specific value
    analytics_service.get_aggregation.return_value = GetAggregationsResponse(values=[])

    client = TestClient(get_router(analytics_service))

    expected_request_obj = GetAggregationsRequest(
        tracker_id='foo',
        where_field='labels',
        where_operator='contains',
        where_values=['whale', 'shark'],
        agg_field='source',
        agg_type='count_bucket_values',
        buckets=['foo', 'bar'],
    )

    response = client.get(
        "/v1/analytics/foo/aggregations?where_field=labels&where_operator=contains&where_values=whale,shark&agg_field=source&agg_type=count_bucket_values&buckets=foo,bar"
    )

    analytics_service.get_aggregation.assert_called_once_with(expected_request_obj)

    assert response.status_code == 200

    assert response.json() == {'values': []}


@pytest.mark.asyncio
async def test_get_analytics_events_stats(analytics_service):
    '''
    Test that the /analytics/:tracker_id/events_stats endpoint returns the correct response
    '''
    analytics_service.get_events_stats.return_value = GetEventsStatsResponse(
        values=[
            EventBucket(
                event='bar',
                sources=[SourceBucket(name='src1', count=14)],
                total_count=44,
            ),
            EventBucket(
                event='baz',
                sources=[SourceBucket(name='src1', count=12)],
                total_count=88,
            ),
        ]
    )

    client = TestClient(get_router(analytics_service))

    expected_request_obj = GetEventsStatsRequest(
        tracker_id='foo',
        events=['bar', 'baz'],
        top_sources_count=4,
    )

    response = client.get(
        "/v1/analytics/foo/events_stats?events=bar,baz&top_sources_count=4"
    )

    analytics_service.get_events_stats.assert_called_once_with(expected_request_obj)

    assert response.status_code == 200

    assert response.json() == {
        'values': [
            {
                'event': 'bar',
                'sources': [{'name': 'src1', 'count': 14}],
                'total_count': 44,
            },
            {
                'event': 'baz',
                'sources': [{'name': 'src1', 'count': 12}],
                'total_count': 88,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_conversion_rate_by_day(client, analytics_service):
    '''
    Test that the /analytics/:tracker_id/conversion endpoint returns the correct response
    '''
    analytics_service.calculate_conversion_rate_by_day.return_value = (
        GetConversionsResponse(
            values=[ConversionPoint(x=1, y=0.5), ConversionPoint(x=2, y=0.6)]
        )
    )

    # Create a TestClient instance
    client = TestClient(get_router(analytics_service))

    # Send a POST request to the /analytics/:tracker_id/conversion endpoint
    response = client.get(
        '/v1/analytics/foo/conversion?event_1=event1&event_2=event2&timestamp_from=100&timestamp_to=200'
    )

    # The expected GetConversionsRequest object that the service method should be called with
    expected_request = GetConversionsRequest(
        tracker_id='foo',
        event_1='event1',
        event_2='event2',
        timestamp_from=100,
        timestamp_to=200,
    )

    # Check the mock was called with the expected arguments
    analytics_service.calculate_conversion_rate_by_day.assert_called_once_with(
        expected_request
    )

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {"values": [{"x": 1, "y": 0.5}, {"x": 2, "y": 0.6}]}
