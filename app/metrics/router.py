from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST

from app.metrics.service import MetricsService


def get_router(metrics_service: MetricsService) -> APIRouter:
    router = APIRouter(prefix="/metrics", tags=["metrics"])

    @router.get("/")
    async def health() -> Response:
        metrics = metrics_service.generate_latest()
        return Response(metrics, headers={"Content-Type": CONTENT_TYPE_LATEST})

    return router
