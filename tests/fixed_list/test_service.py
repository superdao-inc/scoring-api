import io
from typing import Any
import pytest
from unittest.mock import ANY, AsyncMock
from app.common.export import ExportService
from app.fixed_list.repository import FixedListRepository
from app.fixed_list.schemas import (
    GetFixedListAggregationRequest,
    GetFixedListAggregationResponse,
    GetFixedListRequest,
    GetFixedListResponseV2,
    FixedListItem
)
from app.fixed_list.models import FixedListItem as FixedListModel
from app.fixed_list.service import FixedListService


@pytest.fixture
def repository():
    return AsyncMock(FixedListRepository)


@pytest.fixture
def export_service():
    return AsyncMock(spec=ExportService)


@pytest.fixture
def service(repository):
    return FixedListService(repository, export_service)


@pytest.mark.parametrize(
    'list_id, buffer, expected_repo_arg, expected_result',
    [
        (
            'test_list',
            io.BytesIO(b'0x000000000000000000000000000000000000000a'),
            [
                FixedListModel(
                    wallet='0x000000000000000000000000000000000000000a',
                    list_id='test_list'
                )
            ],
            (True, [])
        ),
        (
            'test_list',
            io.BytesIO(b'0x000000000000000000000000000000000000000B'),
            [
                FixedListModel(
                    wallet='0x000000000000000000000000000000000000000b',
                    list_id='test_list'
                )
            ],
            (True, [])
        ),
        (
            'test_list',
            io.BytesIO(b'0xWRONG\n0x000000000000000000000000000000000000000c'),
            [
            ],
            (False, ['0xWRONG'])
        ),
    ]
)
@pytest.mark.asyncio
async def test_save_fixed_list(service, list_id, buffer, expected_repo_arg, expected_result):
    # Arrange

    # Act
    result = await service.save_fixed_list(list_id, buffer)

    # Assert
    assert result == expected_result
    if len(expected_repo_arg) > 0:
        service.repository.save_fixed_list_items.assert_called_once_with(
            ANY
        )
        call_arg = service.repository.save_fixed_list_items.call_args.args[0]
        assert isinstance(call_arg[0], FixedListModel)
        assert call_arg[0].wallet == expected_repo_arg[0].wallet
        assert call_arg[0].list_id == expected_repo_arg[0].list_id


@pytest.mark.asyncio
async def test_get_list_scrolled(service):
    # Arrange
    request = GetFixedListRequest(list_id='test_list')
    items = [
        FixedListItem(
            list_id='test_list',
            wallet='0x123',
        ),
    ]
    has_more = True
    service.repository.get_list.return_value = (items, has_more)

    # Act
    response = await service.get_list_scrolled(request)

    # Assert
    service.repository.get_list.assert_called_once_with(request)
    assert isinstance(response, GetFixedListResponseV2)
    assert response.items == items
    assert response.has_more == has_more


@pytest.mark.asyncio
async def test_get_aggregation(service):
    request = GetFixedListAggregationRequest(
        list_id="test_list",
        agg_type="count",
        agg_field="foo",
        where_field="bar",
        where_values=["biz", "buzz"],
        where_operator="contains",
    )
    expected_response = GetFixedListAggregationResponse(values=[42])
    service.repository.fetch_list_aggregation.return_value = [42]
    response = await service.get_aggregation(request)
    service.repository.fetch_list_aggregation.assert_awaited_once_with(request)
    assert response == expected_response
