import asyncio

from app.claimed.repository import ClaimedRepository
from app.claimed.schemas import (
    ClaimedCSVExportRequest,
    GetClaimedAggregationRequest,
    GetClaimedAggregationResponse,
    GetClaimedRequest,
    GetClaimedResponse,
    GetClaimedResponseV2,
)
from app.common.export import ExportService
from app.common.schemas import AudienceCSVExportResponse


class ClaimedService:
    claimed_repository: ClaimedRepository
    export_service: ExportService

    def __init__(
        self, claimed_repository: ClaimedRepository, export_service: ExportService
    ):
        self.claimed_repository = claimed_repository
        self.export_service = export_service

    async def get_claimed(self, request: GetClaimedRequest) -> GetClaimedResponse:
        items_promise = self.claimed_repository.fetch_claimed(request)
        total_promise = self.claimed_repository.fetch_claimed_count(request)

        items_result, total = await asyncio.gather(items_promise, total_promise)

        items = items_result[0]
        return GetClaimedResponse(items=items, total=total)

    async def get_claimed_scrolled(
        self, request: GetClaimedRequest
    ) -> GetClaimedResponseV2:
        items, has_more = await self.claimed_repository.fetch_claimed(request)
        return GetClaimedResponseV2(items=items, has_more=has_more)

    async def get_aggregation(
        self, request: GetClaimedAggregationRequest
    ) -> GetClaimedAggregationResponse:
        return await self.claimed_repository.fetch_claimed_aggregation(request)

    async def create_csv(
        self, request: ClaimedCSVExportRequest
    ) -> AudienceCSVExportResponse:
        return await asyncio.shield(
            self.export_service.makeAudienceExport(
                request, self.claimed_repository.fetch_claimed
            )
        )
