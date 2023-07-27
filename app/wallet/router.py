from fastapi import APIRouter, Depends

from app.wallet.schemas import (
    GetSimilarWalletsQuery,
    GetSimilarWalletsRequest,
    GetSimilarWalletsResponse,
    GetWalletAttributesRequest,
    GetWalletAttributesResponse,
    GetWalletAttributesSimpleResponse,
    GetWalletsLeaderboardRequest,
    GetWalletsLeaderboardResponse,
)
from app.wallet.service import WalletService


def get_router(wallet_service: WalletService) -> APIRouter:
    router = APIRouter(prefix="/v1/wallet", tags=["wallet"])

    @router.get("/attributes/{address}")
    async def get(address: str) -> GetWalletAttributesResponse:
        request = GetWalletAttributesRequest(wallet=address.lower())
        response = await wallet_service.get_attributes(request)
        response.wallet = address
        return response

    @router.get("/attributes_simple/{address}")
    async def get_simple(address: str) -> GetWalletAttributesSimpleResponse:
        request = GetWalletAttributesRequest(wallet=address.lower())
        response = await wallet_service.get_attributes_simple(request)
        response.wallet = address
        return response

    @router.get("/leaderboard")
    async def get_leaderboard(
        request: GetWalletsLeaderboardRequest = Depends(GetWalletsLeaderboardRequest),
    ) -> GetWalletsLeaderboardResponse:
        response = await wallet_service.get_leaderboard(request)
        return response

    @router.get("/similar/{address}")
    async def get_similar_wallets(
        address: str,
        query: GetSimilarWalletsQuery = Depends(GetSimilarWalletsQuery),
    ) -> GetSimilarWalletsResponse:
        request = GetSimilarWalletsRequest(wallet=address, **query.dict())
        response = await wallet_service.get_similar_wallets(request)
        return response

    return router
