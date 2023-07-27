from app.common.query_builder import AbstractWalletAttributesQueryBuilder
from app.fixed_list.models import FixedListItem
from app.wallet.models import WalletAttributes


class FixedListQueryBuilder(AbstractWalletAttributesQueryBuilder):
    left_model = FixedListItem
    left_model_wallet_address_column = FixedListItem.wallet_b
    left_model_order_columns = []
    left_model_searchable_columns = [FixedListItem.wallet]
    attributes_model_wallet_address_column = WalletAttributes.wallet_b
