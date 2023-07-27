from typing import List

from pydantic import BaseModel

from app.common.schemas import (
    QueryOrderableMixin,
    QueryOverlapMixin,
    QueryPaginationMixin,
    QuerySearchableMixin,
    QueryWhereMixin,
    WalletItemMixin,
)


class GetNftHoldersQuery(
    QueryWhereMixin,
    QueryPaginationMixin,
    QueryOrderableMixin,
    QuerySearchableMixin,
    QueryOverlapMixin,
):
    where_field: str = 'wallet'


class GetNftHoldersRequest(GetNftHoldersQuery):
    collection_address: str


class NftHoldersItem(WalletItemMixin):
    wallet: str


class NftHolderResponse(BaseModel):
    items: List[NftHoldersItem]
    has_more: bool


class GetNftHoldersResponse(NftHolderResponse):
    pass
