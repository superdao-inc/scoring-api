from app.wallet.repository import WalletRepository
from app.wallet.schemas import (
    GetSimilarWalletsAttributesRequest,
    GetSimilarWalletsRequest,
    GetSimilarWalletsResponse,
    GetWalletAttributesRequest,
    GetWalletAttributesResponse,
    GetWalletAttributesSimpleResponse,
    GetWalletsLeaderboardRequest,
    GetWalletsLeaderboardResponse,
)
from app.wallet.similar_wallets_api import SimilarWalletsApi


class WalletService:
    wallet_repository: WalletRepository

    similar_wallets_api: SimilarWalletsApi

    def __init__(
        self,
        wallet_repository: WalletRepository,
        similar_wallets_api: SimilarWalletsApi,
    ):
        self.wallet_repository = wallet_repository
        self.similar_wallets_api = similar_wallets_api

    async def get_attributes(
        self, request: GetWalletAttributesRequest
    ) -> GetWalletAttributesResponse:
        item = await self.wallet_repository.fetch_attributes(request)
        return GetWalletAttributesResponse(**item.dict())

    async def get_attributes_simple(
        self, request: GetWalletAttributesRequest
    ) -> GetWalletAttributesSimpleResponse:
        item = await self.wallet_repository.fetch_attributes(request)
        return GetWalletAttributesSimpleResponse(**item.dict())

    async def get_leaderboard(
        self, request: GetWalletsLeaderboardRequest
    ) -> GetWalletsLeaderboardResponse:
        items = await self.wallet_repository.fetch_leaderboard(request)
        return GetWalletsLeaderboardResponse(items=items)

    async def get_similar_wallets(
        self, request: GetSimilarWalletsRequest
    ) -> GetSimilarWalletsResponse:
        limit = request.limit
        wallet_addresses = await self.similar_wallets_api.get_index_similar_wallets(
            request.wallet, limit
        )
        if not wallet_addresses:
            return GetSimilarWalletsResponse(items=[])

        similar_wallets_data_request = GetSimilarWalletsAttributesRequest(
            similar_wallets=wallet_addresses,
            limit=limit,
        )

        items = await self.wallet_repository.fetch_wallets_attributes(
            similar_wallets_data_request
        )
        return GetSimilarWalletsResponse(items=items)
