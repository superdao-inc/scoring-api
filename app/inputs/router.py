from fastapi import APIRouter

from app.inputs.schemas import GetActivityMetadataResponse
from app.inputs.service import InputsService


def get_router(inputs_service: InputsService) -> APIRouter:
    router = APIRouter(prefix="/v1/inputs", tags=["inputs"])

    @router.get("/activity_metadata")
    async def get_activity_metadata() -> GetActivityMetadataResponse:
        response = await inputs_service.get_activity_metadatas()
        return response

    return router
