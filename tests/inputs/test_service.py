import pytest
from unittest.mock import AsyncMock
from app.inputs.schemas import GetActivityMetadataResponse, ActivityMetadataItem

from app.inputs.repository import ActivityMetadataRepository
from app.inputs.service import InputsService
from app.common.enums import BlockchainType


@pytest.fixture
def activity_metadata_repository():
    return AsyncMock(spec=ActivityMetadataRepository)


@pytest.fixture
def inputs_service(activity_metadata_repository):
    return InputsService(activity_metadata_repository)


@pytest.mark.asyncio
async def test_fetch_activity_metadatas(activity_metadata_repository, inputs_service):
    # Arrange
    activity_metadata_repository.fetch_activity_metadatas.return_value = [
        ActivityMetadataItem(
            address='0xA',
            chain=BlockchainType.ETHEREUM,
            name='A',
            external_url='external_url',
            image_url='image_url',
        )
    ]

    # Act
    response = await inputs_service.get_activity_metadatas()

    # Assert
    activity_metadata_repository.fetch_activity_metadatas.assert_called_once_with()
    assert isinstance(response, GetActivityMetadataResponse)
    assert len(response.items) == 1
