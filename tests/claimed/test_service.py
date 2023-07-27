import pytest
from unittest.mock import AsyncMock
from app.claimed.repository import ClaimedRepository
from app.claimed.schemas import (
    ClaimedItem,
    GetClaimedAggregationRequest,
    GetClaimedAggregationResponse,
    GetClaimedRequest,
    GetClaimedResponse,
    GetClaimedResponseV2,
)
from app.claimed.service import ClaimedService
from app.common.enums import BlockchainType
from app.common.export import ExportService


@pytest.fixture
def claimed_repository():
    return AsyncMock(ClaimedRepository)


@pytest.fixture
def export_service():
    return AsyncMock(spec=ExportService)


@pytest.fixture
def claimed_service(claimed_repository):
    return ClaimedService(claimed_repository, export_service)


@pytest.mark.asyncio
async def test_get_claimed(claimed_service):
    request = GetClaimedRequest(
        claimed_contract="0x1",
        blockchain=None,
        where_field="bar",
        where_values=["biz", "buzz"],
        where_operator="contains",
        search="search_term",
        limit=9,
        offset=10,
    )
    expected_response = GetClaimedResponse(
        items=[
            ClaimedItem(
                wallet="0x1",
                blockchain=BlockchainType.ETHEREUM,
                claimed_contract="0xC",
                claimed_at=1,
                score=42,
            )
        ],
        total=44,
    )
    claimed_service.claimed_repository.fetch_claimed.return_value = (
        expected_response.items,
        True,
    )
    claimed_service.claimed_repository.fetch_claimed_count.return_value = 44

    response = await claimed_service.get_claimed(request)
    claimed_service.claimed_repository.fetch_claimed.assert_awaited_once_with(request)
    claimed_service.claimed_repository.fetch_claimed_count.assert_awaited_once_with(
        request
    )

    assert response == expected_response


@pytest.mark.asyncio
async def test_get_claimed_scrolled(claimed_service):
    # Arrange
    request = GetClaimedRequest(claimed_contract='foo')
    items = [
        ClaimedItem(
            claimed_contract='foo',
            blockchain=BlockchainType.ETHEREUM,
            claimed_at=1,
            score=1.0,
            row_number=2,
            wallet='0x123',
            created_at=42,
        ),
    ]
    has_more = True
    claimed_service.claimed_repository.fetch_claimed.return_value = (items, has_more)

    # Act
    response = await claimed_service.get_claimed_scrolled(request)

    # Assert
    claimed_service.claimed_repository.fetch_claimed.assert_called_once_with(request)
    assert isinstance(response, GetClaimedResponseV2)
    assert response.items == items
    assert response.has_more == has_more


@pytest.mark.asyncio
async def test_get_aggregation(claimed_service):
    request = GetClaimedAggregationRequest(
        claimed_contract="0x1",
        blockchain=None,
        agg_type="count",
        agg_field="foo",
        where_field="bar",
        where_values=["biz", "buzz"],
        where_operator="contains",
    )
    expected_response = GetClaimedAggregationResponse(values=[42])
    claimed_service.claimed_repository.fetch_claimed_aggregation.return_value = (
        expected_response
    )
    response = await claimed_service.get_aggregation(request)
    claimed_service.claimed_repository.fetch_claimed_aggregation.assert_awaited_once_with(
        request
    )
    assert response == expected_response
