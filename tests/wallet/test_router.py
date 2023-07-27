from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.common.schemas import MAX_LIMIT
from app.wallet.router import get_router
from app.wallet.schemas import (
    MAX_SIMILAR_WALLETS_LIMIT,
    GetWalletAttributesRequest,
    GetWalletAttributesResponse,
    GetWalletAttributesSimpleResponse,
    GetWalletsLeaderboardRequest,
    GetWalletsLeaderboardResponse,
    WalletAttributesItem,
    GetSimilarWalletsRequest,
    GetSimilarWalletsResponse,
)
from app.wallet.service import WalletService


@pytest.fixture
def wallet_service():
    return AsyncMock(spec=WalletService)


@pytest.fixture
def client(wallet_service):
    return TestClient(get_router(wallet_service))


@pytest.mark.parametrize(
    "wallet, expected_request, expected_response",
    [
        (
            "0x0123",
            GetWalletAttributesRequest(wallet="0x0123"),
            {
                'wallet': '0x0123',
                'ens_name': None,
                'labels': None,
                'last_month_tx_count': None,
                'nfts_count': None,
                'superrank': None,
                'twitter_username': None,
                'twitter_followers_count': None,
                'twitter_bio': None,
                'wallet_usd_cap': None,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_attributes_simple(
    client, wallet_service, wallet, expected_request, expected_response
):
    # Setup the mock to return a specific value
    wallet_service.get_attributes_simple.return_value = (
        GetWalletAttributesSimpleResponse(wallet=wallet)
    )

    # Send a GET request to the /wallet/attributes endpoint
    response = client.get(f"/v1/wallet/attributes_simple/{wallet}")

    # Check the mock was called with the expected arguments
    wallet_service.get_attributes_simple.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/wallet/attributes/0x1234",
            GetWalletAttributesRequest(wallet="0x1234"),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_attributes(client, wallet_service, path, expected_request):
    # Setup the mock to return a specific value
    wallet_service.get_attributes.return_value = GetWalletAttributesResponse(
        wallet='0x1234'
    )

    # Send a GET request to the /wallet/attributes endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    wallet_service.get_attributes.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {
        'wallet': '0x1234',
        'created_at': None,
        'ens_name': None,
        'labels': None,
        'last_month_tx_count': None,
        'last_month_in_volume': None,
        'last_month_out_volume': None,
        'last_month_volume': None,
        'nfts_count': None,
        'row_number': None,
        'superrank': None,
        'twitter_url': None,
        'twitter_username': None,
        'twitter_avatar_url': None,
        'twitter_followers_count': None,
        'twitter_location': None,
        'twitter_bio': None,
        'tx_count': None,
        'wallet_usd_cap': None,
        'whitelist_activity': None,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/wallet/leaderboard?order_by_field=tx_count&order_by_direction=DESC&limit=10",
            GetWalletsLeaderboardRequest(
                order_by_field='tx_count', order_by_direction='DESC', limit=10
            ),
        ),
        (
            "/v1/wallet/leaderboard?order_by_field=superrank",
            GetWalletsLeaderboardRequest(
                order_by_field='superrank', order_by_direction='ASC', limit=MAX_LIMIT
            ),
        ),
    ],
)
async def test_get_leaderboard(client, wallet_service, path, expected_request):
    # Setup the mock to return a specific value
    wallet_service.get_leaderboard.return_value = GetWalletsLeaderboardResponse(
        items=[WalletAttributesItem(wallet='0x1234')]
    )

    # Send a GET request to the /wallet/leaderboard endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    wallet_service.get_leaderboard.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {
        'items': [
            {
                'wallet': '0x1234',
                'created_at': None,
                'ens_name': None,
                'labels': None,
                'last_month_tx_count': None,
                'last_month_in_volume': None,
                'last_month_out_volume': None,
                'last_month_volume': None,
                'nfts_count': None,
                'row_number': None,
                'superrank': None,
                'twitter_url': None,
                'twitter_username': None,
                'twitter_avatar_url': None,
                'twitter_followers_count': None,
                'twitter_location': None,
                'twitter_bio': None,
                'tx_count': None,
                'wallet_usd_cap': None,
                'whitelist_activity': None,
            }
        ]
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/wallet/similar/0x42?limit=42",
            GetSimilarWalletsRequest(wallet='0x42', limit=42),
        ),
        (
            "/v1/wallet/similar/0x1",
            GetSimilarWalletsRequest(wallet='0x1', limit=MAX_SIMILAR_WALLETS_LIMIT),
        ),
    ],
)
async def test_get_similar_wallets(client, wallet_service, path, expected_request):
    # Setup the mock to return a specific value
    wallet_service.get_similar_wallets.return_value = GetSimilarWalletsResponse(
        items=[WalletAttributesItem(wallet='0x1234')]
    )

    # Send a GET request to the /wallet/leaderboard endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    wallet_service.get_similar_wallets.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {
        'items': [
            {
                'wallet': '0x1234',
                'created_at': None,
                'ens_name': None,
                'labels': None,
                'last_month_tx_count': None,
                'last_month_in_volume': None,
                'last_month_out_volume': None,
                'last_month_volume': None,
                'nfts_count': None,
                'row_number': None,
                'superrank': None,
                'twitter_url': None,
                'twitter_username': None,
                'twitter_avatar_url': None,
                'twitter_followers_count': None,
                'twitter_location': None,
                'twitter_bio': None,
                'tx_count': None,
                'wallet_usd_cap': None,
                'whitelist_activity': None,
            }
        ]
    }
