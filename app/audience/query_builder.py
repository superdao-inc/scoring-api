from app.common.query_builder import AbstractWalletAttributesQueryBuilder
from app.wallet.models import WalletAttributes


class AudienceQueryBuilder(AbstractWalletAttributesQueryBuilder):
    attributes_model_wallet_address_column = WalletAttributes.wallet_b
    left_model = None
    left_model_wallet_address_column = None
    left_model_order_columns = []
    left_model_searchable_columns = []
