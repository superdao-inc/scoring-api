import pytest
from unittest.mock import AsyncMock
from app.wallet.similar_wallets_api import SimilarWalletsApi
from app.wallet.repository import WalletRepository
from app.wallet.schemas import (
    GetSimilarWalletsAttributesRequest,
    GetWalletAttributesRequest,
    GetWalletAttributesResponse,
    GetWalletsLeaderboardRequest,
    GetWalletsLeaderboardResponse,
    GetSimilarWalletsRequest,
    GetSimilarWalletsResponse,
    WalletAttributesItem,
)
from app.wallet.service import WalletService


@pytest.fixture
def wallet_repository():
    return AsyncMock(spec=WalletRepository)


@pytest.fixture
def similar_wallets_api():
    return AsyncMock(spec=SimilarWalletsApi)


@pytest.fixture
def wallet_service(wallet_repository, similar_wallets_api):
    return WalletService(wallet_repository, similar_wallets_api)


@pytest.mark.asyncio
async def test_get_attributes(wallet_repository, wallet_service):
    # Arrange
    request = GetWalletAttributesRequest(wallet='0x1234')
    item = WalletAttributesItem(wallet='0x1234')
    wallet_repository.fetch_attributes.return_value = item

    # Act
    response = await wallet_service.get_attributes(request)

    # Assert
    wallet_repository.fetch_attributes.assert_called_once_with(request)
    assert isinstance(response, GetWalletAttributesResponse)
    assert response.wallet == request.wallet


@pytest.mark.asyncio
async def test_get_leaderboard(wallet_repository, wallet_service):
    # Arrange
    request = GetWalletsLeaderboardRequest(
        order_by_field='wallet_usd_cap', order_by_direction='DESC', limit=10
    )
    item = WalletAttributesItem(wallet='0x1234')
    wallet_repository.fetch_leaderboard.return_value = [item]

    # Act
    response = await wallet_service.get_leaderboard(request)

    # Assert
    wallet_repository.fetch_leaderboard.assert_called_once_with(request)
    assert isinstance(response, GetWalletsLeaderboardResponse)
    assert response.items == [item]


@pytest.mark.asyncio
async def test_get_similar_wallets(
    wallet_repository, wallet_service, similar_wallets_api
):
    request = GetSimilarWalletsRequest(wallet='0x42', limit=25)
    item = WalletAttributesItem(wallet='0x1234')
    wallet_repository.fetch_wallets_attributes.return_value = [item]
    similar_wallets_api.get_index_similar_wallets.return_value = ['0x1234']

    # Act
    response = await wallet_service.get_similar_wallets(request)
    similar_wallets_data_request = GetSimilarWalletsAttributesRequest(
        similar_wallets=['0x1234'], limit=25
    )

    # Assert
    wallet_repository.fetch_wallets_attributes.assert_called_once_with(
        similar_wallets_data_request
    )
    assert isinstance(response, GetSimilarWalletsResponse)
    assert response.items == [item]
