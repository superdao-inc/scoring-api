from app.claimed.models import Claimed
from app.common.query_builder import AbstractWalletAttributesQueryBuilder
from app.wallet.models import WalletAttributes


class ClaimedQueryBuilder(AbstractWalletAttributesQueryBuilder):
    left_model = Claimed
    left_model_wallet_address_column = Claimed.wallet_b
    left_model_order_columns = []
    left_model_searchable_columns = [Claimed.wallet]
    attributes_model_wallet_address_column = WalletAttributes.wallet_b
