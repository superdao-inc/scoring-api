from typing import List, Optional

from pydantic import BaseModel

from app.common.enums import BlockchainType
from app.common.schemas import (
    AudienceCSVExportParams,
    QueryAggregationMixin,
    QueryOrderableMixin,
    QueryOverlapMixin,
    QueryPaginationMixin,
    QuerySearchableMixin,
    QueryWhereMixin,
    WalletItemMixin,
)


class ClaimedItem(WalletItemMixin):
    wallet: str
    blockchain: BlockchainType
    claimed_contract: str
    claimed_at: int


class Claimed(BaseModel):
    items: List[ClaimedItem]
    total: int


class ClaimedV2(BaseModel):
    items: List[ClaimedItem]
    has_more: bool


class GetClaimedQuery(
    QueryWhereMixin,
    QueryPaginationMixin,
    QueryOrderableMixin,
    QuerySearchableMixin,
    QueryOverlapMixin,
):
    pass


class GetClaimedRequest(GetClaimedQuery):
    claimed_contract: str
    blockchain: Optional[BlockchainType] = None


class ClaimedCSVExportRequest(AudienceCSVExportParams, GetClaimedRequest):
    pass


class GetClaimedResponse(Claimed):
    pass


class GetClaimedResponseV2(ClaimedV2):
    pass


class GetClaimedAggregationQuery(
    QueryWhereMixin, QueryAggregationMixin, QuerySearchableMixin, QueryOverlapMixin
):
    pass


class GetClaimedAggregationRequest(GetClaimedAggregationQuery):
    claimed_contract: str
    blockchain: Optional[BlockchainType] = None


class GetClaimedAggregationResponse(BaseModel):
    values: List[int]
