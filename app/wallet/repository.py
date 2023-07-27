from typing import List, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.wallet.mapper import WalletItemMapper
from app.wallet.query_builder import WalletQueryBuilder
from app.wallet.schemas import (
    GetSimilarWalletsAttributesRequest,
    GetWalletAttributesRequest,
    GetWalletsLeaderboardRequest,
    WalletAttributesItem,
)


class WalletRepository:
    session: async_sessionmaker[AsyncSession]
    query_builder: Type[WalletQueryBuilder]
    item_mapper: Type[WalletItemMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        query_builder: Type[WalletQueryBuilder] = WalletQueryBuilder,
        item_mapper: Type[WalletItemMapper] = WalletItemMapper,
    ):
        self.session = session
        self.query_builder = query_builder
        self.item_mapper = item_mapper

    async def fetch_attributes(
        self, request: GetWalletAttributesRequest
    ) -> WalletAttributesItem:
        query = self.query_builder.build_attributes_query(request.wallet)
        async with self.session() as session:
            row = (await session.execute(query)).one_or_none()

        if not row:
            return WalletAttributesItem(wallet=request.wallet)

        return self.item_mapper.map_to_attributes_item(row)

    async def fetch_leaderboard(
        self, request: GetWalletsLeaderboardRequest
    ) -> List[WalletAttributesItem]:
        query = self.query_builder.build_leaderboard_query(
            request.order_by_fields, request.order_by_direction, request.limit
        )
        async with self.session() as session:
            rows = await session.execute(query)

        return [self.item_mapper.map_to_attributes_item(row) for row in rows]

    async def fetch_wallets_attributes(
        self, request: GetSimilarWalletsAttributesRequest
    ) -> List[WalletAttributesItem]:
        query = self.query_builder.build_similar_wallets_attributes_query(
            request.similar_wallets, request.limit
        )

        async with self.session() as session:
            rows = await session.execute(query)

        return [self.item_mapper.map_to_attributes_item(row) for row in rows]
