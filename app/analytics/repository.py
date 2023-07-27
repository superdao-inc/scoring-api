from datetime import datetime
from typing import Any, Dict, List, Tuple, Type, Union

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.analytics.models import AnalyticsEventsCounts, WalletLastEvents
from app.analytics.query_builder import AnalyticsQueryBuilder
from app.analytics.schemas import (
    AnalyticsEventsCountsItem,
    AnalyticsItem,
    GetAggregationsRequest,
    GetAnalyticsRequest,
)
from app.wallet.mapper import WalletItemMapper
from app.wallet.models import WalletAttributes


class AnalyticsRepository:
    session: async_sessionmaker[AsyncSession]
    analytics_query_builder: Type[AnalyticsQueryBuilder]
    wallet_item_mapper: Type[WalletItemMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        analytics_query_builder: Type[AnalyticsQueryBuilder] = AnalyticsQueryBuilder,
        item_mapper: Type[WalletItemMapper] = WalletItemMapper,
    ) -> None:
        self.session = session
        self.analytics_query_builder = analytics_query_builder
        self.wallet_item_mapper = item_mapper

    async def fetch_analytics(
        self, request: GetAnalyticsRequest
    ) -> Tuple[List[AnalyticsItem], int]:
        query = self.analytics_query_builder.build_query(
            [WalletLastEvents.tracker_id == request.tracker_id], request
        )
        total_count_query = self.analytics_query_builder.build_total_count_query(
            [WalletLastEvents.tracker_id == request.tracker_id], request
        )

        async with self.session() as session:
            rows = await session.execute(query)
            rows_count = int(await session.scalar(total_count_query))

        items = [self._map_to_analytics_item(row, request) for row in rows]
        total_count = rows_count

        # we need to limit items here because we request
        # one more item to check if there are more items
        items = items[: request.limit]

        return items, total_count

    async def fetch_analytics_aggregation(
        self, request: GetAggregationsRequest
    ) -> List[int]:
        agg_query = self.analytics_query_builder.build_aggregation_query(
            [WalletLastEvents.tracker_id == request.tracker_id], request
        )

        async with self.session() as session:
            result = await session.execute(agg_query)
            row = result.mappings().first()
            if row:
                values = [int(v or 0) for v in row.values()]
            else:
                values = []

        return values

    async def fetch_events_stats_sources(
        self,
        tracker_id: str,
        top_sources_count: int,
        events: List[str],
    ) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        sources_query = self.analytics_query_builder.build_events_stats_sources_query(
            tracker_id, top_sources_count, events
        )

        async with self.session() as session:
            results = await session.execute(sources_query)
            rows = results.mappings().all() or []

        mapped_results: Dict[str, List[Any]] = {}
        for row in rows:
            event = row['event_type']
            if event not in mapped_results:
                mapped_results[event] = []

            mapped_results[event].append(dict(row))

        return mapped_results

    async def fetch_events_stats_total(
        self,
        tracker_id: str,
        events: List[str],
    ) -> Dict[str, int]:
        query = self.analytics_query_builder.build_events_stats_total_query(
            tracker_id=tracker_id, events=events
        )

        async with self.session() as session:
            result = await session.execute(query)
            rows = result.mappings().all() or []

        mapped_results: Dict[str, int] = {}
        for row in rows:
            mapped_results[row['event_type']] = row['total_count']

        return mapped_results

    def _map_to_analytics_item(
        self,
        row: sa.Row[Tuple[WalletLastEvents, WalletAttributes]],
        request: GetAnalyticsRequest,
    ) -> AnalyticsItem:
        item = AnalyticsItem(
            tracker_id=row.WalletLastEvents.tracker_id,
            wallet=row.WalletLastEvents.address,
            last_event=row.WalletLastEvents.last_event.value,
            last_event_timestamp=row.WalletLastEvents.last_event_timestamp.timestamp(),
            source=row.WalletLastEvents.source,
        )

        return self.wallet_item_mapper.map_wallet_attributes_to(
            row.WalletAttributes, item
        )

    async def fetch_events_counts(
        self,
        event_type_1: str,
        event_type_2: str,
        tracker_id: str,
        timestamp_from: int,
        timestamp_to: int,
    ) -> List[AnalyticsEventsCountsItem]:
        # Fetch all the relevant records for both event types
        recordsQuery = sa.select(AnalyticsEventsCounts).filter(
            AnalyticsEventsCounts.tracker_id == tracker_id,
            AnalyticsEventsCounts.timestamp
            >= datetime.utcfromtimestamp(timestamp_from),
            AnalyticsEventsCounts.timestamp <= datetime.utcfromtimestamp(timestamp_to),
            AnalyticsEventsCounts.event_type.in_([event_type_1, event_type_2]),
        )

        async with self.session() as session:
            result = await session.execute(recordsQuery)
            rows = result.all()

        records = [self._map_to_events_counts_item(row) for row in rows]

        return records

    def _map_to_events_counts_item(
        self,
        row: sa.Row[Tuple[AnalyticsEventsCounts]],
    ) -> AnalyticsEventsCountsItem:
        item = AnalyticsEventsCountsItem(
            tracker_id=row.AnalyticsEventsCounts.tracker_id,
            event_type=row.AnalyticsEventsCounts.event_type,
            timestamp=row.AnalyticsEventsCounts.timestamp.timestamp(),
            count=row.AnalyticsEventsCounts.count,
        )

        return item
