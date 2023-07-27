from typing import Optional

from fastapi import APIRouter, Depends

from app.analytics.schemas import (
    GetAggregationsQuery,
    GetAggregationsRequest,
    GetAggregationsResponse,
    GetAnalyticsQuery,
    GetAnalyticsRequest,
    GetAnalyticsResponse,
    GetConversionsQuery,
    GetConversionsRequest,
    GetConversionsResponse,
    GetEventsStatsQuery,
    GetEventsStatsRequest,
    GetEventsStatsResponse,
)
from app.analytics.service import AnalyticsService


def get_router(analytics_service: AnalyticsService) -> APIRouter:
    router = APIRouter(prefix="/v1/analytics", tags=["analytics"])

    @router.get("/{tracker_id}")
    async def get(
        tracker_id: str, query: GetAnalyticsQuery = Depends(GetAnalyticsQuery)
    ) -> GetAnalyticsResponse:
        request = GetAnalyticsRequest(tracker_id=tracker_id, **query.dict())

        response = await analytics_service.get_analytics(request)
        return response

    @router.get("/{tracker_id}/aggregations", tags=["analytics"])
    async def get_aggregations(
        tracker_id: str,
        query: Optional[GetAggregationsQuery] = Depends(GetAggregationsQuery),
    ) -> GetAggregationsResponse:
        request = GetAggregationsRequest(
            tracker_id=tracker_id, **(query.dict() if query else {})
        )

        response = await analytics_service.get_aggregation(request)
        return response

    @router.get("/{tracker_id}/events_stats", tags=["analytics"])
    async def get_events_stats(
        tracker_id: str,
        query: Optional[GetEventsStatsQuery] = Depends(GetEventsStatsQuery),
    ) -> GetEventsStatsResponse:
        request = GetEventsStatsRequest(
            tracker_id=tracker_id, **query.dict() if query else {}
        )

        response = await analytics_service.get_events_stats(request)

        return response

    @router.get("/{tracker_id}/conversion", tags=["analytics"])
    async def get_conversion_rate_by_day(
        tracker_id: str,
        query: GetConversionsQuery = Depends(GetConversionsQuery),
    ) -> GetConversionsResponse:
        request = GetConversionsRequest(tracker_id=tracker_id, **query.dict())

        response = await analytics_service.calculate_conversion_rate_by_day(request)

        return response

    return router
