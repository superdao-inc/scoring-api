from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.inputs.service import InputsService
from app.inputs.router import get_router
from app.inputs.schemas import GetActivityMetadataResponse, ActivityMetadataItem
from app.common.enums import BlockchainType


@pytest.fixture
def inputs_service():
    return AsyncMock(spec=InputsService)


@pytest.fixture
def client(inputs_service):
    return TestClient(get_router(inputs_service))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path, service_return_value, expected_json",
    [
        (
            "/v1/inputs/activity_metadata",
            GetActivityMetadataResponse(
                items=[
                    ActivityMetadataItem(
                        address='0xA',
                        chain=BlockchainType.ETHEREUM,
                        name='A',
                        external_url='external_url',
                        image_url='image_url',
                    )
                ]
            ),
            {
                'items': [
                    {
                        'address': '0xA',
                        'chain': 'ETHEREUM',
                        'name': 'A',
                        'external_url': 'external_url',
                        'image_url': 'image_url',
                    }
                ]
            },
        )
    ],
)
async def test_get_activity_metadatas(
    client, inputs_service, path, service_return_value, expected_json
):
    # Setup the mock to return a specific value
    inputs_service.get_activity_metadatas.return_value = service_return_value

    # Send a GET request to the /dictionary endpoint
    response = client.get(path)

    # Check the mock was called with the expected arguments
    inputs_service.get_activity_metadatas.assert_called_once_with()

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == expected_json
