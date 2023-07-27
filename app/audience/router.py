from typing import Optional

from fastapi import APIRouter, Depends

from app.audience.schemas import (
    AudienceCSVExportParams,
    AudienceCSVExportRequest,
    GetAudienceAggregationQuery,
    GetAudienceAggregationRequest,
    GetAudienceAggregationResponse,
    GetAudienceQuery,
    GetAudienceRequest,
    GetAudienceResponse,
    GetAudienceResponseV2,
)
from app.audience.service import AudienceService
from app.common.schemas import AudienceCSVExportResponse


def map_audience_score_id_to_audience_name(score_id: str) -> str:
    if score_id == 'crypto_natives_score':
        return 'audience:early_adopters'

    if score_id.startswith("label:"):
        return score_id[6:]
    if score_id.endswith("_score"):
        return f"audience:{score_id[:-6]}"

    return score_id


def get_router(audience_service: AudienceService) -> APIRouter:
    router = APIRouter(prefix="/v1/audience", tags=["audience"], deprecated=True)

    @router.get("/{score_id}")
    async def get(
        score_id: str,
        query: Optional[GetAudienceQuery] = Depends(GetAudienceQuery),
    ) -> GetAudienceResponse:
        audience_name = map_audience_score_id_to_audience_name(score_id)

        request = GetAudienceRequest(
            audience_name=audience_name, **(query.dict() if query else {})
        )

        response = await audience_service.get_audience(request)
        return response

    @router.post("/{score_id}/export-csv", tags=["audience"])
    async def csv_export(
        score_id: str, exportParams: AudienceCSVExportParams
    ) -> AudienceCSVExportResponse:
        audience_name = map_audience_score_id_to_audience_name(score_id)

        request = AudienceCSVExportRequest(
            audience_name=audience_name, **exportParams.dict()
        )

        response = await audience_service.create_csv(request)

        return response

    @router.get("/{score_id}/aggregation")
    async def get_aggregation(
        score_id: str,
        query: GetAudienceAggregationQuery = Depends(),
    ) -> GetAudienceAggregationResponse:
        audience_name = map_audience_score_id_to_audience_name(score_id)

        request = GetAudienceAggregationRequest(
            audience_name=audience_name, **query.dict()
        )
        return await audience_service.get_aggregation(request)

    return router


def get_router_v2(audience_service: AudienceService) -> APIRouter:
    router = APIRouter(prefix="/v2/audience", tags=["audience"], deprecated=True)

    @router.get("/{score_id}")
    async def get(
        score_id: str,
        query: Optional[GetAudienceQuery] = Depends(GetAudienceQuery),
    ) -> GetAudienceResponseV2:
        audience_name = map_audience_score_id_to_audience_name(score_id)

        request = GetAudienceRequest(
            audience_name=audience_name, **(query.dict() if query else {})
        )

        response = await audience_service.get_audience_scrolled(request)
        return response

    return router


def get_router_v3(audience_service: AudienceService) -> APIRouter:
    router = APIRouter(prefix="/v3/audience", tags=["audience"])

    @router.get("/{audience_name}")
    async def get(
        audience_name: str,
        query: Optional[GetAudienceQuery] = Depends(GetAudienceQuery),
    ) -> GetAudienceResponseV2:
        request = GetAudienceRequest(
            audience_name=audience_name, **(query.dict() if query else {})
        )

        response = await audience_service.get_audience_scrolled(request)
        return response

    @router.post("/{audience_name}/export-csv", tags=["audience"])
    async def csv_export(
        audience_name: str, exportParams: AudienceCSVExportParams
    ) -> AudienceCSVExportResponse:
        request = AudienceCSVExportRequest(
            audience_name=audience_name, **exportParams.dict()
        )

        response = await audience_service.create_csv(request)

        return response

    @router.get("/{audience_name}/aggregation")
    async def get_aggregation(
        audience_name: str,
        query: GetAudienceAggregationQuery = Depends(),
    ) -> GetAudienceAggregationResponse:
        request = GetAudienceAggregationRequest(
            audience_name=audience_name, **query.dict()
        )
        return await audience_service.get_aggregation(request)

    return router
