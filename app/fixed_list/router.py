from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile

from app.common.schemas import AudienceCSVExportParams, AudienceCSVExportResponse
from app.fixed_list.schemas import (
    CreateFixedListResponse,
    FixedCSVExportRequest,
    GetFixedListAggregationQuery,
    GetFixedListAggregationRequest,
    GetFixedListAggregationResponse,
    GetFixedListQuery,
    GetFixedListRequest,
    GetFixedListResponseV2,
)
from app.fixed_list.service import FixedListService


def get_router(fixed_list_service: FixedListService) -> APIRouter:
    router = APIRouter(prefix="/v1/fixed_list", tags=["fixed_list"])

    @router.post("/")
    async def create(
        file: UploadFile,
        list_id: str = Form(...),
    ) -> CreateFixedListResponse:
        result, invalid_wallets = await fixed_list_service.save_fixed_list(
            list_id, file.file
        )

        response = (
            CreateFixedListResponse(result=result, list_id=list_id)
            if result
            else CreateFixedListResponse(
                result=result, list_id=list_id, invalid_wallets=invalid_wallets
            )
        )

        return response

    @router.get("/{list_id}/aggregation")
    async def get_aggregation(
        list_id: str,
        query: Optional[GetFixedListAggregationQuery] = Depends(
            GetFixedListAggregationQuery
        ),
    ) -> GetFixedListAggregationResponse:
        request = GetFixedListAggregationRequest(
            list_id=list_id, **(query.dict() if query else {})
        )
        return await fixed_list_service.get_aggregation(request)

    return router


def get_router_v2(fixed_list_service: FixedListService) -> APIRouter:
    router = APIRouter(prefix="/v2/fixed_list", tags=["fixed_list"])

    @router.get("/{list_id}")
    async def get(
        list_id: str,
        query: Optional[GetFixedListQuery] = Depends(GetFixedListQuery),
    ) -> GetFixedListResponseV2:
        request = GetFixedListRequest(
            list_id=list_id, **(query.dict() if query else {})
        )
        response = await fixed_list_service.get_list_scrolled(request)
        return response

    @router.post("/{list_id}/export-csv")
    async def csv_export(
        list_id: str,
        exportParams: AudienceCSVExportParams,
    ) -> AudienceCSVExportResponse:
        request = FixedCSVExportRequest(list_id=list_id, **exportParams.dict())

        response = await fixed_list_service.create_csv(request)
        return response

    return router
