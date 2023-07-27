from datetime import datetime
from unittest.mock import AsyncMock
import pytest
from app.common.enums import AudienceType, BlockchainType
from app.top_collections.models import TopCollectionsModel
from app.top_collections.schemas import (
    TopCollectionsItem,
    TopCollectionsQuery,
    TopCollectionsResponse,
)

from app.top_collections.service import TopCollectionsService


@pytest.fixture
def top_collections_repo():
    return AsyncMock(spec=TopCollectionsService)


@pytest.fixture
def top_collections_service(top_collections_repo):
    return TopCollectionsService(top_collections_repo)


@pytest.mark.asyncio
async def test_get_top_collections(top_collections_service, top_collections_repo):
    # Arrange
    query = TopCollectionsQuery(
        audience_id='foo',
        audience_type=AudienceType.CLAIMED,
        top_n=1,
        blockchain=BlockchainType.ETHEREUM,
    )
    repo_result = [
        TopCollectionsModel(
            audience_slug='foo',
            audience_type=AudienceType.CLAIMED,
            chain=BlockchainType.ETHEREUM,
            token_address='0x1234',
            nft_count=1,
            updated=datetime.fromtimestamp(100),
            holders_count=10,
        )
    ]

    expected_response = TopCollectionsResponse(
        items=[
            TopCollectionsItem(
                audience_id='foo',
                audience_type='claimed',
                blockchain='eth',
                contract_address='0x1234',
                nfts_count=1,
                updated=100,
                holders_count=10,
                total_holders_count=0,
                total_nfts_count=0,
            )
        ]
    )

    top_collections_repo.get_top_collections.return_value = repo_result

    # Act
    response = await top_collections_service.get_top_collections(query)

    # Assert
    top_collections_repo.get_top_collections.assert_called_once_with(
        query.audience_id,
        query.audience_type,
        query.blockchain,
        query.top_n,
        query.order_by_field,
        query.order_by_direction,
        query.use_whitelisted_activities
    )
    assert isinstance(response, TopCollectionsResponse)
    assert response == expected_response
