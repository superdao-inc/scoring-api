from typing import List, Tuple, Type

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.audience.query_builder import AudienceQueryBuilder
from app.audience.schemas import (
    AudienceItem,
    GetAudienceAggregationRequest,
    GetAudienceAggregationResponse,
    GetAudienceRequest,
)
from app.wallet.mapper import WalletItemMapper
from app.wallet.models import WalletAttributes


class AudienceRepository:
    session: async_sessionmaker[AsyncSession]
    audience_query_builder: Type[AudienceQueryBuilder]
    wallet_item_mapper: Type[WalletItemMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        audience_query_builder: Type[AudienceQueryBuilder] = AudienceQueryBuilder,
        item_mapper: Type[WalletItemMapper] = WalletItemMapper,
    ):
        self.session = session
        self.audience_query_builder = audience_query_builder
        self.wallet_item_mapper = item_mapper

    async def fetch_audience(
        self, request: GetAudienceRequest
    ) -> Tuple[List[AudienceItem], bool]:
        async with self.session() as session:
            rows = await session.execute(
                self.audience_query_builder.build_query(
                    [WalletAttributes.labels.contains([request.audience_name])],
                    request,
                )
            )

        items = [self._map_to_audience_item(row, request) for row in rows]
        has_more = (len(items) > request.limit) if request.limit else False

        # we need to limit items here because we request
        # one more item to check if there are more items
        items = items[: request.limit]

        return items, has_more

    async def fetch_audience_count(self, request: GetAudienceRequest) -> int:
        total_count_query = self.audience_query_builder.build_total_count_query(
            [WalletAttributes.labels.contains([request.audience_name])], request
        )

        async with self.session() as session:
            rows_count = int(await session.scalar(total_count_query))

        return rows_count

    async def fetch_audience_aggregation(
        self, request: GetAudienceAggregationRequest
    ) -> GetAudienceAggregationResponse:
        agg_query = self.audience_query_builder.build_aggregation_query(
            [WalletAttributes.labels.contains([request.audience_name])], request
        )

        async with self.session() as session:
            result = await session.execute(agg_query)
            row = result.mappings().first()
            if row:
                values = [int(v or 0) for v in row.values()]
            else:
                values = []

        return GetAudienceAggregationResponse(values=values)

    def _map_to_audience_item(
        self,
        row: sa.Row[Tuple[WalletAttributes]],
        request: GetAudienceRequest,
    ) -> AudienceItem:
        item = AudienceItem(
            score_id='0',
            score=0,
            wallet=row.WalletAttributes.wallet,
        )

        return self.wallet_item_mapper.map_wallet_attributes_to(
            row.WalletAttributes, item
        )
