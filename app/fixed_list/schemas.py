from typing import List, Optional

from pydantic import BaseModel

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


class FixedListItem(WalletItemMixin):
    wallet: str
    list_id: str


class FixedListV2(BaseModel):
    items: List[FixedListItem]
    has_more: bool


class GetFixedListQuery(
    QueryWhereMixin,
    QueryPaginationMixin,
    QueryOrderableMixin,
    QuerySearchableMixin,
    QueryOverlapMixin,
):
    pass


class GetFixedListRequest(GetFixedListQuery):
    list_id: str


class FixedCSVExportRequest(AudienceCSVExportParams, GetFixedListRequest):
    pass


class GetFixedListResponseV2(FixedListV2):
    pass


class GetFixedListAggregationQuery(
    QueryWhereMixin, QueryAggregationMixin, QuerySearchableMixin, QueryOverlapMixin
):
    pass


class GetFixedListAggregationRequest(GetFixedListAggregationQuery):
    list_id: str


class GetFixedListAggregationResponse(BaseModel):
    values: List[int]


class CreateFixedListResponse(BaseModel):
    result: bool
    list_id: Optional[str] = None
    invalid_wallets: Optional[List[str]] = []
