from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field, validator

MAX_LIMIT = 1000


class QueryWhereMixin(BaseModel):
    where_field: Optional[str] = None
    where_operator: Optional[Literal["contains", "eq", "ne", "overlap"]] = None
    where_values: Optional[Any] = None

    def __init__(self, **data):  # type: ignore
        if isinstance(data.get('where_values'), str):
            data['where_values'] = [b.strip() for b in data['where_values'].split(",")]

        super().__init__(**data)


class QueryPaginationMixin(BaseModel):
    ignore_max_limit: bool = False
    limit: Optional[int] = MAX_LIMIT
    offset: Optional[int] = Field(None, ge=0)

    @validator("limit", pre=True)
    def validate_limit(cls, v: int, values) -> int:  # type: ignore
        if values['ignore_max_limit']:
            return v
        if 0 < v <= MAX_LIMIT:
            return v
        else:
            raise ValueError('must be in range')


class QueryOrderableMixin(BaseModel):
    order_by_field: Optional[str] = None  # deprecated
    order_by_fields: Optional[Any] = None
    order_by_direction: Optional[Literal["ASC", "DESC"]] = None

    def __init__(self, **data):  # type: ignore
        if isinstance(data.get('order_by_field'), str):
            data['order_by_fields'] = [data['order_by_field']]
        elif isinstance(data.get('order_by_fields'), str):
            data['order_by_fields'] = [
                b.strip() for b in data['order_by_fields'].split(",")
            ]

        super().__init__(**data)


class QuerySearchableMixin(BaseModel):
    search: Optional[str] = None


class QueryAggregationMixin(BaseModel):
    agg_type: Literal["count", "sum", "count_bucket_intervals", "count_bucket_values"]
    agg_field: str

    buckets: Optional[Any] = None

    def __init__(self, **data):  # type: ignore
        if isinstance(data.get('buckets'), str):
            data['buckets'] = [b.strip() for b in data['buckets'].split(",")]

        super().__init__(**data)


class QueryOverlapMixin(BaseModel):
    overlap_audiences: Optional[Any] = None

    def __init__(self, **data):  # type: ignore
        if isinstance(data.get('overlap_audiences'), str):
            data['overlap_audiences'] = [
                c.strip() for c in data['overlap_audiences'].split(",")
            ]

        super().__init__(**data)


class WalletItemMixin(BaseModel):
    superrank: Optional[int] = None
    created_at: Optional[int] = None
    tx_count: Optional[int] = None
    last_month_tx_count: Optional[int] = None
    last_month_in_volume: Optional[int] = None
    last_month_out_volume: Optional[int] = None
    last_month_volume: Optional[int] = None
    nfts_count: Optional[int] = None
    ens_name: Optional[str] = None
    twitter_url: Optional[str] = None
    twitter_username: Optional[str] = None
    twitter_avatar_url: Optional[str] = None
    twitter_followers_count: Optional[int] = None
    twitter_location: Optional[str] = None
    twitter_bio: Optional[str] = None
    wallet_usd_cap: Optional[int] = None
    labels: Optional[List[str]] = None
    whitelist_activity: Optional[List[str]] = None


class CSVExportColumn(BaseModel):
    key: str
    nice_name: str


class AudienceCSVExportParams(
    QueryWhereMixin, QueryPaginationMixin, QueryOrderableMixin, QuerySearchableMixin
):
    fields: list[CSVExportColumn]
    file_name: str


class AudienceCSVExportResponse(BaseModel):
    uploaded_file_url: Optional[str]
