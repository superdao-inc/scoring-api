from typing import Any, List, Optional

from pydantic import BaseModel

from app.common.schemas import (
    QueryAggregationMixin,
    QueryOrderableMixin,
    QueryOverlapMixin,
    QueryPaginationMixin,
    QuerySearchableMixin,
    QueryWhereMixin,
    WalletItemMixin,
)


class AnalyticsItem(WalletItemMixin):
    tracker_id: str
    wallet: str
    last_event: str
    last_event_timestamp: int
    source: Optional[str] = None

    class Config:
        orm_mode = True


class Analytics(BaseModel):
    items: List[AnalyticsItem]
    total: int


class GetAnalyticsQuery(
    QueryWhereMixin,
    QueryPaginationMixin,
    QueryOrderableMixin,
    QuerySearchableMixin,
    QueryOverlapMixin,
):
    pass


class GetAnalyticsRequest(GetAnalyticsQuery):
    tracker_id: str


class GetAnalyticsResponse(Analytics):
    pass


class GetAggregationsQuery(
    QueryWhereMixin, QueryAggregationMixin, QuerySearchableMixin, QueryOverlapMixin
):
    pass


class GetAggregationsRequest(GetAggregationsQuery):
    tracker_id: str


class GetAggregationsResponse(BaseModel):
    values: List[int]


class GetEventsStatsQuery(BaseModel):
    events: Optional[Any]
    top_sources_count: Optional[int]

    def __init__(self, **data):  # type: ignore
        if isinstance(data.get('events'), str):
            data['events'] = [b.strip() for b in data['events'].split(",")]

        super().__init__(**data)


class GetEventsStatsRequest(GetEventsStatsQuery):
    tracker_id: str


class GetConversionsQuery(BaseModel):
    event_1: str
    event_2: str
    timestamp_from: int
    timestamp_to: int


class GetConversionsRequest(GetConversionsQuery):
    tracker_id: str


class AnalyticsEventsCountsItem(BaseModel):
    tracker_id: str
    event_type: str
    timestamp: int
    count: int


class ConversionPoint(BaseModel):
    x: int
    y: float


class GetConversionsResponse(BaseModel):
    values: List[ConversionPoint]


class SourceBucket(BaseModel):
    name: str
    count: int


class EventBucket(BaseModel):
    event: str
    sources: List[SourceBucket]
    total_count: int


class GetEventsStatsResponse(BaseModel):
    values: List[EventBucket]
