from typing import Optional

from fastapi import APIRouter, Depends

from app.claimed.schemas import (
    ClaimedCSVExportRequest,
    GetClaimedAggregationQuery,
    GetClaimedAggregationRequest,
    GetClaimedAggregationResponse,
    GetClaimedQuery,
    GetClaimedRequest,
    GetClaimedResponse,
    GetClaimedResponseV2,
)
from app.claimed.service import ClaimedService
from app.common.enums import BlockchainType
from app.common.schemas import AudienceCSVExportParams, AudienceCSVExportResponse


def get_router(claimed_service: ClaimedService) -> APIRouter:
    router = APIRouter(prefix="/v1/claimed", tags=["claimed"])

    @router.get("/{claimed_contract}/aggregation")
    @router.get("/{claimed_contract}/aggregation/{blockchain}")
    async def get_aggregation(
        claimed_contract: str,
        blockchain: Optional[BlockchainType] = None,
        query: Optional[GetClaimedAggregationQuery] = Depends(
            GetClaimedAggregationQuery
        ),
    ) -> GetClaimedAggregationResponse:
        request = GetClaimedAggregationRequest(
            claimed_contract=claimed_contract,
            blockchain=blockchain,
            **(query.dict() if query else {})
        )
        return await claimed_service.get_aggregation(request)

    @router.get("/{claimed_contract}/{blockchain}")
    @router.get("/{claimed_contract}")
    async def get(
        claimed_contract: str,
        blockchain: Optional[BlockchainType] = None,
        query: Optional[GetClaimedQuery] = Depends(GetClaimedQuery),
    ) -> GetClaimedResponse:
        request = GetClaimedRequest(
            claimed_contract=claimed_contract,
            blockchain=blockchain,
            **(query.dict() if query else {})
        )
        response = await claimed_service.get_claimed(request)
        return response

    @router.post("/{claimed_contract}/{blockchain}/export-csv")
    @router.post("/{claimed_contract}/export-csv")
    async def csv_export(
        claimed_contract: str,
        exportParams: AudienceCSVExportParams,
        blockchain: Optional[BlockchainType] = None,
    ) -> AudienceCSVExportResponse:
        request = ClaimedCSVExportRequest(
            claimed_contract=claimed_contract,
            blockchain=blockchain,
            **exportParams.dict()
        )

        response = await claimed_service.create_csv(request)
        return response

    return router


def get_router_v2(claimed_service: ClaimedService) -> APIRouter:
    router = APIRouter(prefix="/v2/claimed", tags=["claimed"])

    @router.get("/{claimed_contract}/{blockchain}")
    @router.get("/{claimed_contract}")
    async def get(
        claimed_contract: str,
        blockchain: Optional[BlockchainType] = None,
        query: Optional[GetClaimedQuery] = Depends(GetClaimedQuery),
    ) -> GetClaimedResponseV2:
        request = GetClaimedRequest(
            claimed_contract=claimed_contract,
            blockchain=blockchain,
            **(query.dict() if query else {})
        )
        response = await claimed_service.get_claimed_scrolled(request)
        return response

    return router
