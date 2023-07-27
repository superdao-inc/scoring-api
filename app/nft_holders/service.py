from app.nft_holders.repository import NftHoldersRepository
from app.nft_holders.schemas import GetNftHoldersRequest, GetNftHoldersResponse


class NftHoldersService:
    nft_holders_repository: NftHoldersRepository

    def __init__(self, overlapping_repository: NftHoldersRepository):
        self.nft_holders_repository = overlapping_repository

    async def get_nft_holders_scrolled(
        self, request: GetNftHoldersRequest
    ) -> GetNftHoldersResponse:
        items, has_more = await self.nft_holders_repository.fetch_nft_holders(request)

        return GetNftHoldersResponse(items=items, has_more=has_more)
