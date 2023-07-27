from fastapi import APIRouter, Depends

from app.top_collections.schemas import TopCollectionsQuery, TopCollectionsResponse
from app.top_collections.service import TopCollectionsService


def get_router(top_collections_service: TopCollectionsService) -> APIRouter:
    router = APIRouter(prefix="/v1/top-collections", tags=["top-collections"])

    @router.get('/')
    async def get_top_collections(
        query: TopCollectionsQuery = Depends(TopCollectionsQuery),
    ) -> TopCollectionsResponse:
        response = await top_collections_service.get_top_collections(query)

        return response

    return router
