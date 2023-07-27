from typing import List, Tuple, Type

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.nft_holders.models import NftHolders
from app.nft_holders.query_builder import NftHoldersQueryBuilder
from app.nft_holders.schemas import GetNftHoldersRequest, NftHoldersItem
from app.wallet.mapper import WalletItemMapper
from app.wallet.models import WalletAttributes


class NftHoldersRepository:
    session: async_sessionmaker[AsyncSession]
    nft_holders_query_builder: Type[NftHoldersQueryBuilder]
    wallet_item_mapper: Type[WalletItemMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        nft_holders_query_builder: Type[
            NftHoldersQueryBuilder
        ] = NftHoldersQueryBuilder,
        item_mapper: Type[WalletItemMapper] = WalletItemMapper,
    ) -> None:
        self.session = session
        self.nft_holders_query_builder = nft_holders_query_builder
        self.wallet_item_mapper = item_mapper

    async def fetch_nft_holders(
        self, request: GetNftHoldersRequest
    ) -> Tuple[List[NftHoldersItem], bool]:
        async with self.session() as session:
            token_contract = request.collection_address
            contract_prefix = request.collection_address[:3]
            query = self.nft_holders_query_builder.build_query(
                [
                    NftHolders.token_contract == token_contract,
                    NftHolders.contract_prefix == contract_prefix,
                ],
                request,
            )

            rows = await session.execute(query)

        items = [self._map_to_overlap_audience(row) for row in rows]
        has_more = (len(items) > request.limit) if request.limit else False

        # we need to limit items here because we request
        # one more item to check if there are more items
        items = items[: request.limit]

        return items, has_more

    def _map_to_overlap_audience(
        self,
        row: sa.Row[Tuple[NftHolders, WalletAttributes]],
    ) -> NftHoldersItem:
        item = NftHoldersItem(
            wallet=row.NftHolders.wallet,
        )

        return self.wallet_item_mapper.map_wallet_attributes_to(
            row.WalletAttributes, item
        )
