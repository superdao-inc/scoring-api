from typing import List, Tuple, Type

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.claimed.models import Claimed
from app.claimed.query_builder import ClaimedQueryBuilder
from app.claimed.schemas import (
    ClaimedItem,
    GetClaimedAggregationRequest,
    GetClaimedAggregationResponse,
    GetClaimedRequest,
)
from app.wallet.mapper import WalletItemMapper
from app.wallet.models import WalletAttributes


class ClaimedRepository:
    session: async_sessionmaker[AsyncSession]
    claimed_query_builder: Type[ClaimedQueryBuilder]
    wallet_item_mapper: Type[WalletItemMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        claimed_query_builder: Type[ClaimedQueryBuilder] = ClaimedQueryBuilder,
        item_mapper: Type[WalletItemMapper] = WalletItemMapper,
    ):
        self.session = session
        self.claimed_query_builder = claimed_query_builder
        self.wallet_item_mapper = item_mapper

    async def fetch_claimed(
        self, request: GetClaimedRequest
    ) -> Tuple[List[ClaimedItem], bool]:
        async with self.session() as session:
            custom_where_clause = [Claimed.claimed_contract == request.claimed_contract]
            if request.blockchain:
                custom_where_clause.append(Claimed.blockchain == request.blockchain)

            rows = await session.execute(
                self.claimed_query_builder.build_query(custom_where_clause, request)
            )

        items = [self._map_to_claimed_item(row, request) for row in rows]
        has_more = (len(items) > request.limit) if request.limit else False

        # we need to limit items here because we request
        # one more item to check if there are more items
        items = items[: request.limit]

        return items, has_more

    async def fetch_claimed_count(self, request: GetClaimedRequest) -> int:
        custom_where_clause = [Claimed.claimed_contract == request.claimed_contract]
        if request.blockchain:
            custom_where_clause.append(Claimed.blockchain == request.blockchain)

        total_count_query = self.claimed_query_builder.build_total_count_query(
            custom_where_clause, request
        )

        async with self.session() as session:
            rows_count = int(await session.scalar(total_count_query))

        return rows_count

    async def fetch_claimed_aggregation(
        self, request: GetClaimedAggregationRequest
    ) -> GetClaimedAggregationResponse:
        custom_where_clause = [Claimed.claimed_contract == request.claimed_contract]
        if request.blockchain:
            custom_where_clause.append(Claimed.blockchain == request.blockchain)

        agg_query = self.claimed_query_builder.build_aggregation_query(
            custom_where_clause, request
        )

        async with self.session() as session:
            result = await session.execute(agg_query)
            row = result.mappings().first()
            if row:
                values = [int(v or 0) for v in row.values()]
            else:
                values = []

        return GetClaimedAggregationResponse(values=values)

    def _map_to_claimed_item(
        self,
        row: sa.Row[Tuple[Claimed, WalletAttributes]],
        request: GetClaimedRequest,
    ) -> ClaimedItem:
        item = ClaimedItem(
            wallet=row.Claimed.wallet,
            blockchain=row.Claimed.blockchain,
            claimed_contract=row.Claimed.claimed_contract,
            claimed_at=1,
        )

        return self.wallet_item_mapper.map_wallet_attributes_to(
            row.WalletAttributes, item
        )
