from typing import List, Tuple, Type

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.fixed_list.models import FixedListItem as FixedListItemModel
from app.fixed_list.query_builder import FixedListQueryBuilder
from app.fixed_list.schemas import (
    FixedListItem,
    GetFixedListAggregationRequest,
    GetFixedListRequest,
)
from app.wallet.mapper import WalletItemMapper
from app.wallet.models import WalletAttributes


class FixedListRepository:
    session: async_sessionmaker[AsyncSession]
    query_builder: Type[FixedListQueryBuilder]
    wallet_item_mapper: Type[WalletItemMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        query_builder: Type[FixedListQueryBuilder] = FixedListQueryBuilder,
        wallet_item_mapper: Type[WalletItemMapper] = WalletItemMapper,
    ):
        self.session = session
        self.query_builder = query_builder
        self.wallet_item_mapper = wallet_item_mapper

    async def save_fixed_list_items(self, records: List[FixedListItemModel]) -> None:
        async with self.session() as session:
            recs = [
                {
                    "list_id": record.list_id,
                    "wallet": record.wallet,
                    "wallet_b": sa.func.decode(
                        sa.func.substring(record.wallet, 3), 'hex'
                    ),
                }
                for record in records
            ]

            await session.execute(
                pg_insert(FixedListItemModel)  # type: ignore
                .values(recs)
                .on_conflict_do_nothing()
            )
            await session.commit()

    async def get_list(
        self, request: GetFixedListRequest
    ) -> Tuple[List[FixedListItem], bool]:
        async with self.session() as session:
            rows = await session.execute(
                self.query_builder.build_query(
                    [FixedListItemModel.list_id == request.list_id], request
                )
            )

        items = [self._map_to_model(row) for row in rows]
        has_more = (len(items) > request.limit) if request.limit else False

        # we need to limit items here because we request
        # one more item to check if there are more items
        items = items[: request.limit]

        return items, has_more

    async def get_list_count(self, request: GetFixedListRequest) -> int:
        total_count_query = self.query_builder.build_total_count_query(
            [FixedListItemModel.list_id == request.list_id], request
        )

        async with self.session() as session:
            rows_count = int(await session.scalar(total_count_query))

        return rows_count

    async def fetch_list_aggregation(
        self, request: GetFixedListAggregationRequest
    ) -> List[int]:
        agg_query = self.query_builder.build_aggregation_query(
            [FixedListItemModel.list_id == request.list_id], request
        )

        async with self.session() as session:
            result = await session.execute(agg_query)
            row = result.mappings().first()
            if row:
                values = [int(v or 0) for v in row.values()]
            else:
                values = []

        return values

    def _map_to_model(
        self,
        row: sa.Row[Tuple[FixedListItem, WalletAttributes]],
    ) -> FixedListItem:
        item = FixedListItem(
            wallet=row.FixedListItem.wallet,
            list_id=row.FixedListItem.list_id,
        )

        return self.wallet_item_mapper.map_wallet_attributes_to(
            row.WalletAttributes, item
        )
