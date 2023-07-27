import pytest
from unittest.mock import AsyncMock
from app.nft_holders.repository import NftHoldersRepository
from app.nft_holders.schemas import (
    NftHoldersItem,
    GetNftHoldersRequest,
    GetNftHoldersResponse,
)
from app.nft_holders.service import NftHoldersService


@pytest.fixture
def nft_holders_repository():
    return AsyncMock(NftHoldersRepository)


@pytest.fixture
def nft_holders_service(nft_holders_repository):
    return NftHoldersService(nft_holders_repository)


@pytest.mark.asyncio
async def test_get_nft_holders_scrolled(nft_holders_service):
    # Arrange
    request = GetNftHoldersRequest(collection_address='foo')
    items = [
        NftHoldersItem(
            claimed_at=1,
            score=1.0,
            row_number=2,
            wallet='0x123',
            created_at=42,
        ),
    ]
    has_more = True
    nft_holders_service.nft_holders_repository.fetch_nft_holders.return_value = (
        items,
        has_more,
    )

    # Act
    response = await nft_holders_service.get_nft_holders_scrolled(request)

    # Assert
    nft_holders_service.nft_holders_repository.fetch_nft_holders.assert_called_once_with(
        request
    )
    assert isinstance(response, GetNftHoldersResponse)
    assert response.items == items
    assert response.has_more == has_more
