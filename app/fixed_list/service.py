import asyncio
import codecs
import csv
from typing import BinaryIO, List, Tuple

from eth_utils import is_address

from app.common.export import ExportService
from app.common.schemas import AudienceCSVExportResponse
from app.fixed_list.models import FixedListItem
from app.fixed_list.repository import FixedListRepository
from app.fixed_list.schemas import (
    FixedCSVExportRequest,
    GetFixedListAggregationRequest,
    GetFixedListAggregationResponse,
    GetFixedListRequest,
    GetFixedListResponseV2,
)

LIST_SAVE_BATCH_SIZE = 100


class FixedListService:
    repository: FixedListRepository
    export_service: ExportService

    def __init__(
        self, repository: FixedListRepository, export_service: ExportService
    ) -> None:
        self.repository = repository
        self.export_service = export_service

    async def save_fixed_list(
        self, list_id: str, file: BinaryIO
    ) -> Tuple[bool, List[str]]:
        invalid_wallets = []
        write_buffer: List[FixedListItem] = []
        iterator = codecs.iterdecode(file, 'utf-8')
        csvReader = csv.reader(iterator)
        for row in csvReader:
            if not is_address(row[0]):
                invalid_wallets.append(row[0])

        if len(invalid_wallets) > 0:
            return False, invalid_wallets

        file.seek(0)
        csvReader = csv.reader(codecs.iterdecode(file, 'utf-8'))
        for row in csvReader:
            write_buffer.append(FixedListItem(wallet=row[0].lower(), list_id=list_id))
            if len(write_buffer) == LIST_SAVE_BATCH_SIZE:
                await self.repository.save_fixed_list_items(write_buffer)
                write_buffer.clear()

        await self.repository.save_fixed_list_items(write_buffer)

        return True, []

    async def get_list_scrolled(
        self, request: GetFixedListRequest
    ) -> GetFixedListResponseV2:
        items, has_more = await self.repository.get_list(request)

        return GetFixedListResponseV2(items=items, has_more=has_more)

    async def get_aggregation(
        self, request: GetFixedListAggregationRequest
    ) -> GetFixedListAggregationResponse:
        buckets = await self.repository.fetch_list_aggregation(request)

        return GetFixedListAggregationResponse(values=buckets)

    async def create_csv(
        self, request: FixedCSVExportRequest
    ) -> AudienceCSVExportResponse:
        return await asyncio.shield(
            self.export_service.makeAudienceExport(request, self.repository.get_list)
        )
