from asyncio import gather
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List

from app.analytics.repository import AnalyticsRepository
from app.analytics.schemas import (
    ConversionPoint,
    EventBucket,
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

DEFAULT_TOP_SOURCES_COUNT = 5


class AnalyticsService:
    analytics_repository: AnalyticsRepository

    def __init__(self, analytics_repository: AnalyticsRepository) -> None:
        self.analytics_repository = analytics_repository

    async def get_analytics(self, request: GetAnalyticsRequest) -> GetAnalyticsResponse:
        items, total = await self.analytics_repository.fetch_analytics(request)

        return GetAnalyticsResponse(items=items, total=total)

    async def get_aggregation(
        self, request: GetAggregationsRequest
    ) -> GetAggregationsResponse:
        aggregated_values = await self.analytics_repository.fetch_analytics_aggregation(
            request=request
        )

        return GetAggregationsResponse(values=aggregated_values)

    async def get_events_stats(
        self, request: GetEventsStatsRequest
    ) -> GetEventsStatsResponse:
        promises = [
            self.analytics_repository.fetch_events_stats_sources(
                request.tracker_id,
                request.top_sources_count
                if request.top_sources_count
                else DEFAULT_TOP_SOURCES_COUNT,
                request.events if request.events else [],
            ),
            self.analytics_repository.fetch_events_stats_total(
                request.tracker_id, request.events if request.events else []
            ),
        ]

        results = await gather(*promises)

        sources = results[0]
        total = results[1]

        event_buckets: Dict[str, Any] = {}

        for event_name, sources in sources.items():
            total_count = total[event_name] if event_name in total else 0
            event = (
                EventBucket(event=event_name, sources=[], total_count=total_count)
                if event_name not in event_buckets
                else event_buckets[event_name]
            )

            event.sources.extend(
                [
                    SourceBucket(name=row['source'], count=row['count'])
                    for row in sources
                ]
            )

            event_buckets[event_name] = event

        return GetEventsStatsResponse(values=[*event_buckets.values()])

    async def calculate_conversion_rate_by_day(
        self, request: GetConversionsRequest
    ) -> GetConversionsResponse:
        event_type_1 = request.event_1
        event_type_2 = request.event_2

        records = await self.analytics_repository.fetch_events_counts(
            event_type_1,
            event_type_2,
            request.tracker_id,
            request.timestamp_from,
            request.timestamp_to,
        )

        counters: DefaultDict[int, Dict[str, int]] = defaultdict(
            lambda: {event_type_1: 0, event_type_2: 0}
        )
        for record in records:
            counters[record.timestamp][record.event_type] += record.count

        # Compute the ratios for each day
        ratios: List[ConversionPoint] = []
        for timestamp, counts in counters.items():
            if counts[event_type_2] > 0:
                ratio = round((counts[event_type_1] / counts[event_type_2]) * 100, 2)
            else:
                ratio = 0
            ratios.append(ConversionPoint(x=timestamp, y=ratio))

        # Sort by timestamp
        ratios.sort(key=lambda point: point.x)

        return GetConversionsResponse(values=ratios)
