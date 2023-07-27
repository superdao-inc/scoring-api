from typing import List

import sqlalchemy as sa

from app.analytics.models import AnalyticsEventsSources, WalletLastEvents
from app.common.query_builder import AbstractWalletAttributesQueryBuilder


class AnalyticsQueryBuilder(AbstractWalletAttributesQueryBuilder):
    left_model = WalletLastEvents
    left_model_wallet_address_column = WalletLastEvents.address
    left_model_order_columns = []
    left_model_searchable_columns = [WalletLastEvents.address]

    @classmethod
    def build_events_stats_sources_query(
        self, tracker_id: str, top_sources_count: int, events: List[str]
    ) -> sa.Select:
        query = (
            sa.select(
                AnalyticsEventsSources.tracker_id,
                AnalyticsEventsSources.event_type,
                AnalyticsEventsSources.source,
                AnalyticsEventsSources.count,
            )
            .where(AnalyticsEventsSources.tracker_id == tracker_id)
            .where(
                AnalyticsEventsSources.event_type.in_(events)
                if len(events) > 0
                else sa.sql.true()
            )
            .where(
                AnalyticsEventsSources.source.in_(
                    sa.select(AnalyticsEventsSources.source)
                    .where(AnalyticsEventsSources.tracker_id == tracker_id)
                    .where(AnalyticsEventsSources.source != '')
                    .group_by(AnalyticsEventsSources.source)
                    .order_by(sa.func.sum(AnalyticsEventsSources.count).desc())
                    .limit(top_sources_count)
                )
            )
        )

        return query

    @classmethod
    def build_events_stats_total_query(
        self, tracker_id: str, events: List[str]
    ) -> sa.Select:
        query = (
            sa.select(
                AnalyticsEventsSources.event_type,
                sa.func.sum(AnalyticsEventsSources.count).label('total_count'),
            )
            .where(
                AnalyticsEventsSources.tracker_id == tracker_id,
            )
            .where(
                AnalyticsEventsSources.event_type.in_(events)
                if len(events) > 0
                else sa.sql.true()
            )
            .group_by(
                AnalyticsEventsSources.tracker_id, AnalyticsEventsSources.event_type
            )
        )

        return query
