import asyncio

from app.audience.repository import AudienceRepository
from app.audience.schemas import (
    AudienceCSVExportRequest,
    GetAudienceAggregationRequest,
    GetAudienceAggregationResponse,
    GetAudienceRequest,
    GetAudienceResponse,
    GetAudienceResponseV2,
)
from app.common.export import ExportService
from app.common.schemas import AudienceCSVExportResponse


class AudienceService:
    audience_repository: AudienceRepository
    export_service: ExportService

    def __init__(
        self,
        audience_repository: AudienceRepository,
        export_service: ExportService,
    ):
        self.audience_repository = audience_repository
        self.export_service = export_service

    async def get_audience(self, request: GetAudienceRequest) -> GetAudienceResponse:
        audience_promise = self.audience_repository.fetch_audience(request)
        total_count_promise = self.audience_repository.fetch_audience_count(request)

        audience_results, total = await asyncio.gather(
            audience_promise, total_count_promise
        )

        items = audience_results[0]
        return GetAudienceResponse(items=items, total=total)

    async def get_audience_scrolled(
        self, request: GetAudienceRequest
    ) -> GetAudienceResponseV2:
        audience, has_more = await self.audience_repository.fetch_audience(request)
        return GetAudienceResponseV2(items=audience, has_more=has_more)

    async def create_csv(
        self, request: AudienceCSVExportRequest
    ) -> AudienceCSVExportResponse:
        return await asyncio.shield(
            self.export_service.makeAudienceExport(
                request, self.audience_repository.fetch_audience
            )
        )

    async def get_aggregation(
        self, request: GetAudienceAggregationRequest
    ) -> GetAudienceAggregationResponse:
        return await self.audience_repository.fetch_audience_aggregation(request)
