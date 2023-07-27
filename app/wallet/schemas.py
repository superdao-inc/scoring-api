from typing import Any, List, Literal, Optional

from pydantic import BaseModel

from app.common.schemas import MAX_LIMIT


class WalletAttributesSimple(BaseModel):
    wallet: str
    superrank: Optional[int] = None
    labels: Optional[List[str]] = None
    last_month_tx_count: Optional[int] = None
    nfts_count: Optional[int] = None
    ens_name: Optional[str] = None
    twitter_username: Optional[str] = None
    twitter_followers_count: Optional[int] = None
    twitter_bio: Optional[str] = None
    wallet_usd_cap: Optional[int] = None


class WalletAttributesItem(BaseModel):
    wallet: str
    superrank: Optional[int] = None
    row_number: Optional[int] = None
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


class GetWalletAttributesRequest(BaseModel):
    wallet: str


class GetWalletAttributesSimpleResponse(WalletAttributesSimple):
    pass


class GetWalletAttributesResponse(WalletAttributesItem):
    pass


class GetWalletsLeaderboardRequest(BaseModel):
    order_by_field: Optional[str] = None  # deprecated
    order_by_fields: Optional[Any] = None
    order_by_direction: Literal["ASC", "DESC"] = "ASC"
    limit: Optional[int] = MAX_LIMIT

    def __init__(self, **data):  # type: ignore
        if isinstance(data.get('order_by_field'), str):
            data['order_by_fields'] = [data['order_by_field']]
        elif isinstance(data.get('order_by_fields'), str):
            data['order_by_fields'] = [
                b.strip() for b in data['order_by_fields'].split(",")
            ]

        super().__init__(**data)


class GetWalletsLeaderboardResponse(BaseModel):
    items: List[WalletAttributesItem]


MAX_SIMILAR_WALLETS_LIMIT = 20


class GetSimilarWalletsQuery(BaseModel):
    limit: Optional[int] = MAX_SIMILAR_WALLETS_LIMIT


class GetSimilarWalletsRequest(GetSimilarWalletsQuery):
    wallet: str


class GetSimilarWalletsAttributesRequest(GetSimilarWalletsQuery):
    similar_wallets: List[str]


class GetSimilarWalletsResponse(BaseModel):
    items: List[WalletAttributesItem]
