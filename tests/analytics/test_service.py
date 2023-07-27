import pytest
from unittest.mock import AsyncMock
from app.analytics.repository import AnalyticsRepository
from app.analytics.schemas import (
    AnalyticsEventsCountsItem,
    ConversionPoint,
    EventBucket,
    AnalyticsItem,
    GetAggregationsRequest,
    GetAggregationsResponse,
    GetAnalyticsRequest,
    GetAnalyticsResponse,
    GetConversionsRequest,
    GetConversionsResponse,
    GetEventsStatsRequest,
    GetEventsStatsResponse,
    SourceBucket,
)
from app.analytics.service import AnalyticsService


@pytest.fixture
def analytics_repository():
    return AsyncMock(spec=AnalyticsRepository)


@pytest.fixture
def analytics_service(analytics_repository):
    return AnalyticsService(analytics_repository)


@pytest.mark.asyncio
async def test_get_analytics(analytics_service, analytics_repository):
    # Arrange
    request = GetAnalyticsRequest(tracker_id='foo')
    items = [
        AnalyticsItem(
            tracker_id='foo',
            last_event='FORM_SUBMIT',
            last_event_timestamp=125,
            wallet='0x123',
            score=12,
        ),
        AnalyticsItem(
            tracker_id='foo',
            last_event='WALLET_CONNECT',
            last_event_timestamp=123,
            wallet='0x124',
            score=13,
        ),
    ]
    total = 5
    analytics_repository.fetch_analytics.return_value = (items, total)

    # Act
    response = await analytics_service.get_analytics(request)

    # Assert
    analytics_repository.fetch_analytics.assert_called_once_with(request)
    assert isinstance(response, GetAnalyticsResponse)
    assert response.items == items
    assert response.total == total


@pytest.mark.asyncio
async def test_get_audience_aggregation(analytics_service, analytics_repository):
    # Arrange
    request = GetAggregationsRequest(tracker_id='foo', agg_type='sum', agg_field='bar')
    values = [1, 2, 3]
    analytics_repository.fetch_analytics_aggregation.return_value = values

    # Act
    response = await analytics_service.get_aggregation(request)

    # Assert
    analytics_repository.fetch_analytics_aggregation.assert_called_once_with(
        request=request
    )
    assert isinstance(response, GetAggregationsResponse)
    assert response.values == values


@pytest.mark.asyncio
async def test_get_events_stats(analytics_service, analytics_repository):
    request = GetEventsStatsRequest(
        tracker_id='foo', events='bar,baz', top_sources_count=4
    )
    sources_rows = {
        'bar': [
            {'event_type': 'bar', 'source': 'google', 'count': 14},
            {'event_type': 'bar', 'source': 'superdao', 'count': 15},
        ],
        'baz': [
            {'event_type': 'baz', 'source': 'google', 'count': 16},
            {'event_type': 'baz', 'source': 'superdao', 'count': 17},
        ],
    }

    total_rows = {
        'bar': 111,
        'baz': 222,
    }

    analytics_repository.fetch_events_stats_sources.return_value = sources_rows
    analytics_repository.fetch_events_stats_total.return_value = total_rows

    expected_response_values = [
        EventBucket(
            event='bar',
            sources=[
                SourceBucket(name='google', count=14),
                SourceBucket(name='superdao', count=15),
            ],
            total_count=111,
        ),
        EventBucket(
            event='baz',
            sources=[
                SourceBucket(name='google', count=16),
                SourceBucket(name='superdao', count=17),
            ],
            total_count=222,
        ),
    ]

    response = await analytics_service.get_events_stats(request)

    analytics_repository.fetch_events_stats_sources.assert_called_once_with(
        'foo', 4, ['bar', 'baz']
    )
    assert isinstance(response, GetEventsStatsResponse)
    assert response.values == expected_response_values


@pytest.mark.asyncio
async def test_сalculate_conversion_rate_by_day(
    analytics_service, analytics_repository
):
    request = GetConversionsRequest(
        tracker_id='foo',
        event_1='event1',
        event_2='event2',
        timestamp_from=1,
        timestamp_to=2,
    )

    records_1 = [
        AnalyticsEventsCountsItem(
            event_type='event1', timestamp=1, count=10, tracker_id='foo'
        ),
        AnalyticsEventsCountsItem(
            event_type='event2', timestamp=1, count=40, tracker_id='foo'
        ),
    ]

    analytics_repository.fetch_events_counts.side_effect = [
        records_1,
    ]

    # Act
    response = await analytics_service.calculate_conversion_rate_by_day(request)

    assert isinstance(response, GetConversionsResponse)

    expected_values = [ConversionPoint(x=1, y=25.0)]
    assert response.values == expected_values
