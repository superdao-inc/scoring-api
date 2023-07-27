from app.common.query_builder import AbstractWalletAttributesQueryBuilder
from app.nft_holders.models import NftHolders
from app.wallet.models import WalletAttributes


class NftHoldersQueryBuilder(AbstractWalletAttributesQueryBuilder):
    left_model = NftHolders
    left_model_wallet_address_column = NftHolders.wallet_b
    left_model_order_columns = []
    left_model_searchable_columns = [NftHolders.wallet]
    attributes_model_wallet_address_column = WalletAttributes.wallet_b
