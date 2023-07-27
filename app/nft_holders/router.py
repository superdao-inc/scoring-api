from typing import Optional

from fastapi import APIRouter, Depends

from app.nft_holders.schemas import (
    GetNftHoldersQuery,
    GetNftHoldersRequest,
    GetNftHoldersResponse,
)
from app.nft_holders.service import NftHoldersService


def get_router(nft_holders_service: NftHoldersService) -> APIRouter:
    router = APIRouter(prefix="/v1/nft_holders", tags=["overlapping"])

    @router.get("/{collection_address}")
    async def get(
        collection_address: str,
        query: Optional[GetNftHoldersQuery] = Depends(GetNftHoldersQuery),
    ) -> GetNftHoldersResponse:
        request = GetNftHoldersRequest(
            collection_address=collection_address, **(query.dict() if query else {})
        )

        response = await nft_holders_service.get_nft_holders_scrolled(request)

        return response

    return router
