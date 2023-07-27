from typing import Any, Tuple, TypeVar

import sqlalchemy as sa

from app.wallet.models import WalletAttributes
from app.wallet.schemas import WalletAttributesItem

T = TypeVar("T", bound=Any)


class WalletItemMapper:
    @classmethod
    def map_wallet_attributes_to(cls, obj: WalletAttributes, item: T) -> T:
        if not obj:
            return cls.fill_default_values(item)

        item.superrank = obj.superrank
        item.created_at = obj.created_at.timestamp() if obj.created_at else None
        item.tx_count = obj.tx_count
        item.last_month_tx_count = obj.last_month_tx_count
        item.last_month_in_volume = obj.last_month_in_volume
        item.last_month_out_volume = obj.last_month_out_volume
        item.last_month_volume = obj.last_month_volume
        item.nfts_count = obj.nfts_count
        item.ens_name = obj.ens_name
        item.twitter_url = obj.twitter_url
        item.twitter_username = obj.twitter_username
        item.twitter_avatar_url = obj.twitter_avatar_url
        item.twitter_followers_count = obj.twitter_followers_count
        item.twitter_location = obj.twitter_location
        item.twitter_bio = obj.twitter_bio
        item.wallet_usd_cap = obj.wallet_usd_cap
        item.labels = obj.labels
        item.whitelist_activity = obj.whitelist_activity

        return item

    @classmethod
    def map_to_attributes_item(
        cls,
        row: sa.Row[Tuple[WalletAttributes]],
    ) -> WalletAttributesItem:
        return cls.map_wallet_attributes_to(
            row.WalletAttributes,
            WalletAttributesItem(wallet=row.WalletAttributes.wallet),
        )

    @classmethod
    def fill_default_values(cls, item: T) -> T:
        item.superrank = 0
        item.wallet_usd_cap = 0
        item.tx_count = 0
        item.last_month_tx_count = 0
        item.last_month_in_volume = 0
        item.last_month_out_volume = 0
        item.last_month_volume = 0
        item.nfts_count = 0

        return item
