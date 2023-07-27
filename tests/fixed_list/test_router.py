from typing import Any, Dict, List, Tuple
from unittest.mock import AsyncMock

from fastapi import FastAPI

import pytest

from fastapi.testclient import TestClient


from app.fixed_list.schemas import (
    GetFixedListAggregationRequest,
    GetFixedListAggregationResponse,
    GetFixedListRequest,
    GetFixedListResponseV2,
)
from app.fixed_list.service import FixedListService

from app.fixed_list.router import get_router, get_router_v2


@pytest.fixture
def fixed_list_service():
    return AsyncMock(FixedListService)


@pytest.fixture
def client_v1(fixed_list_service: AsyncMock):
    # for testing POST request we need FastAPI object
    app = FastAPI()
    app.include_router(get_router(fixed_list_service))

    return TestClient(app=app)


@pytest.fixture
def client_v2(fixed_list_service: AsyncMock):
    return TestClient(get_router_v2(fixed_list_service))


@pytest.mark.parametrize(
    "path, expected_request",
    [
        ("/v2/fixed_list/list_1", GetFixedListRequest(list_id="list_1")),
        (
            "/v2/fixed_list/list_1?where_field=bar&where_values=biz,buzz&where_operator=contains&search=search_term&limit=9&offset=10",
            GetFixedListRequest(
                list_id="list_1",
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                search="search_term",
                limit=9,
                offset=10,
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_fixed_list_v2(client_v2, fixed_list_service, path, expected_request):
    # Setup the mock to return a specific value
    fixed_list_service.get_list_scrolled.return_value = GetFixedListResponseV2(
        items=[], has_more=False
    )

    # Send a GET request to the endpoint
    response = client_v2.get(path)

    # Check the mock was called with the expected arguments
    fixed_list_service.get_list_scrolled.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'items': [], 'has_more': False}


@pytest.mark.parametrize(
    "path, expected_request",
    [
        (
            "/v1/fixed_list/list_2/aggregation?agg_type=count&agg_field=bar",
            GetFixedListAggregationRequest(
                list_id="list_2",
                agg_type="count",
                agg_field="bar",
            ),
        ),
        (
            "/v1/fixed_list/list_2/aggregation?agg_type=count_bucket_values&&agg_field=bar&where_field=bar&where_values=biz,buzz&where_operator=contains&buckets=1,2",
            GetFixedListAggregationRequest(
                list_id="list_2",
                agg_type="count_bucket_values",
                agg_field="bar",
                where_field="bar",
                where_values=["biz", "buzz"],
                where_operator="contains",
                buckets=['1', '2'],
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_aggregation(client_v1, fixed_list_service, path, expected_request):
    # Setup the mock to return a specific value
    fixed_list_service.get_aggregation.return_value = GetFixedListAggregationResponse(
        values=[1, 2]
    )

    # Send a GET request to the endpoint
    response = client_v1.get(path)

    # Check the mock was called with the expected arguments
    fixed_list_service.get_aggregation.assert_called_once_with(expected_request)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response body is correct
    assert response.json() == {'values': [1, 2]}


@pytest.mark.parametrize(
    'list_id,service_result,expected_response',
    [
        (
            'test_list',
            (True, []),
            {
                'result': True,
                'list_id': 'test_list',
                'invalid_wallets': [],
            },
        ),
        (
            'test_list',
            (False, ['0x0000000000000000000000000000000000000000']),
            {
                'result': False,
                'list_id': 'test_list',
                'invalid_wallets': ['0x0000000000000000000000000000000000000000'],
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_list(
    client_v1: TestClient,
    fixed_list_service: AsyncMock,
    list_id: str,
    service_result: Tuple[bool, List[str]],
    expected_response: Dict[str, Any],
):
    fixed_list_service.save_fixed_list.return_value = service_result

    response = client_v1.post(
        "/v1/fixed_list",
        data={"list_id": list_id},
        files={
            "file": (
                "test_wallets.csv",
                "0x0000000000000000000000000000000000000000,\n0x0000000000000000000000000000000000000001",
            )
        },
        headers={"X-Token": "blablabla"},
    )

    assert response.status_code == 200
    assert response.json() == expected_response
