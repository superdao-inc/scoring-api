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


class AudienceItem(WalletItemMixin):
    wallet: str
    score_id: str
    score: int
    row_number: Optional[int] = None

    class Config:
        orm_mode = True


class Audience(BaseModel):
    items: List[AudienceItem]
    total: int


class AudienceV2(BaseModel):
    items: List[AudienceItem]
    has_more: bool


class GetAudienceQuery(
    QueryWhereMixin,
    QueryPaginationMixin,
    QueryOrderableMixin,
    QuerySearchableMixin,
    QueryOverlapMixin,
):
    pass


class GetAudienceRequest(GetAudienceQuery):
    audience_name: str
    score_id: Optional[str]  # deprecated


class AudienceCSVExportRequest(AudienceCSVExportParams, GetAudienceRequest):
    pass


class GetAudienceResponse(Audience):
    pass


class GetAudienceResponseV2(AudienceV2):
    pass


class GetAudienceAggregationQuery(
    QueryWhereMixin, QueryAggregationMixin, QuerySearchableMixin, QueryOverlapMixin
):
    pass


class GetAudienceAggregationRequest(GetAudienceAggregationQuery):
    audience_name: str
    score_id: Optional[str]  # deprecated


class GetAudienceAggregationResponse(BaseModel):
    values: List[int]
