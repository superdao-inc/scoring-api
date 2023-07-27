import pytest
from unittest.mock import AsyncMock
from app.audience.repository import AudienceRepository
from app.audience.schemas import (
    AudienceItem,
    GetAudienceAggregationRequest,
    GetAudienceAggregationResponse,
    GetAudienceRequest,
    GetAudienceResponse,
    GetAudienceResponseV2,
)
from app.audience.service import AudienceService
from app.common.export import ExportService


@pytest.fixture
def audience_repository():
    return AsyncMock(spec=AudienceRepository)


@pytest.fixture
def export_service():
    return AsyncMock(spec=ExportService)


@pytest.fixture
def audience_service(audience_repository):
    return AudienceService(audience_repository, export_service)


@pytest.mark.asyncio
async def test_get_audience_scrolled(audience_service, audience_repository):
    # Arrange
    request = GetAudienceRequest(audience_name='foo')
    items = [
        AudienceItem(
            score_id='0', score=0, row_number=2, wallet='0x123', created_at=42
        ),
        AudienceItem(
            score_id='0', score=0, row_number=1, wallet='0x124', created_at=42
        ),
    ]
    has_more = True
    audience_repository.fetch_audience.return_value = (items, has_more)

    # Act
    response = await audience_service.get_audience_scrolled(request)

    # Assert
    audience_repository.fetch_audience.assert_called_once_with(request)
    assert isinstance(response, GetAudienceResponseV2)
    assert response.items == items
    assert response.has_more == has_more


@pytest.mark.asyncio
async def test_get_audience(audience_service, audience_repository):
    # Arrange
    request = GetAudienceRequest(audience_name='foo')
    items = [
        AudienceItem(
            score_id='0', score=0, row_number=2, wallet='0x123', created_at=42
        ),
        AudienceItem(
            score_id='0', score=0, row_number=1, wallet='0x124', created_at=42
        ),
    ]
    total = 44
    audience_repository.fetch_audience.return_value = (items, True)
    audience_repository.fetch_audience_count.return_value = total

    # Act
    response = await audience_service.get_audience(request)

    # Assert
    audience_repository.fetch_audience.assert_called_once_with(request)
    assert isinstance(response, GetAudienceResponse)
    assert response.items == items
    assert response.total == total


@pytest.mark.asyncio
async def test_get_audience_aggregation(audience_service, audience_repository):
    # Arrange
    request = GetAudienceAggregationRequest(
        audience_name='foo', agg_type='sum', agg_field='bar'
    )
    values = GetAudienceAggregationResponse(values=[1, 2, 3])
    audience_repository.fetch_audience_aggregation.return_value = values

    # Act
    response = await audience_service.get_aggregation(request)

    # Assert
    audience_repository.fetch_audience_aggregation.assert_called_once_with(request)
    assert isinstance(response, GetAudienceAggregationResponse)
    assert response.values == values.values
