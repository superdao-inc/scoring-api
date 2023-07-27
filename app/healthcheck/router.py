from fastapi import APIRouter

from app.healthcheck.service import HealthCheckService


def get_router(healthcheck: HealthCheckService) -> APIRouter:
    router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])

    @router.get("/")
    async def health() -> dict[str, str]:
        return await healthcheck.health()

    return router
