import datetime
from unittest.mock import MagicMock
import pytest

from app.inputs.models import ActivityMetadata
from app.inputs.mapper import ActivityMetadataMapper
from app.inputs.schemas import ActivityMetadataItem
from app.common.enums import BlockchainType


@pytest.fixture
def mapper():
    return ActivityMetadataMapper


@pytest.fixture
def activity_metadata_objects():
    return [
        MagicMock(
            ActivityMetadata=ActivityMetadata(
                address='0xA',
                chain=BlockchainType.ETHEREUM,
                name='A',
                external_url='external_url_a',
                image_url='image_url_a',
            )
        ),
        MagicMock(
            ActivityMetadata=ActivityMetadata(
                address='0xB',
                chain=BlockchainType.POLYGON,
                name='B',
                external_url='external_url_b',
                image_url='image_url_b',
            )
        ),
    ]


def test_map_to_activity_metadata_items(mapper, activity_metadata_objects):
    items = mapper.map_to_activity_metadata_items(activity_metadata_objects)

    assert all(isinstance(item, ActivityMetadataItem) for item in items)

    assert items == [
        ActivityMetadataItem(
            address='0xA',
            chain=BlockchainType.ETHEREUM,
            name='A',
            external_url='external_url_a',
            image_url='image_url_a',
        ),
        ActivityMetadataItem(
            address='0xB',
            chain=BlockchainType.POLYGON,
            name='B',
            external_url='external_url_b',
            image_url='image_url_b',
        ),
    ]
