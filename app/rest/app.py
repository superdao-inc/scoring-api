from fastapi import APIRouter, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.metrics.middleware import MetricsMiddleware
from app.rest.error_handlers import value_error_exception_handler
from app.settings.settings import Settings


class RestApp:
    settings: Settings
    session: async_sessionmaker[AsyncSession]
    app: FastAPI

    healthcheck_router: APIRouter
    audience_router: APIRouter
    audience_v2_router: APIRouter
    audience_v3_router: APIRouter
    analytics_router: APIRouter
    wallet_router: APIRouter
    claimed_router: APIRouter
    claimed_v2_router: APIRouter
    fixed_list_router: APIRouter
    fixed_list_v2_router: APIRouter
    top_collections_router: APIRouter
    dictionary_router: APIRouter
    inputs_router: APIRouter
    nft_holders_router: APIRouter

    metrics_router: APIRouter

    def __init__(
        self,
        settings: Settings,
        session: async_sessionmaker[AsyncSession],
        app: FastAPI,
        healthcheck_router: APIRouter,
        audience_router: APIRouter,
        audience_v2_router: APIRouter,
        audience_v3_router: APIRouter,
        analytics_router: APIRouter,
        wallet_router: APIRouter,
        claimed_router: APIRouter,
        claimed_v2_router: APIRouter,
        fixed_list_router: APIRouter,
        fixed_list_v2_router: APIRouter,
        top_collections_router: APIRouter,
        dictionary_router: APIRouter,
        inputs_router: APIRouter,
        nft_holders_router: APIRouter,
        # prometheus metrics
        metrics_router: APIRouter,
    ) -> None:
        self.settings = settings
        self.session = session
        self.app = app

        self.healthcheck_router = healthcheck_router
        self.audience_router = audience_router
        self.audience_v2_router = audience_v2_router
        self.audience_v3_router = audience_v3_router
        self.analytics_router = analytics_router
        self.wallet_router = wallet_router
        self.claimed_router = claimed_router
        self.claimed_v2_router = claimed_v2_router
        self.fixed_list_router = fixed_list_router
        self.fixed_list_v2_router = fixed_list_v2_router
        self.top_collections_router = top_collections_router
        self.dictionary_router = dictionary_router
        self.inputs_router = inputs_router
        self.nft_holders_router = nft_holders_router

        self.metrics_router = metrics_router

    def include_routers(self) -> None:
        self.app.include_router(self.healthcheck_router)
        self.app.include_router(self.audience_router)
        self.app.include_router(self.audience_v2_router)
        self.app.include_router(self.audience_v3_router)
        self.app.include_router(self.analytics_router)
        self.app.include_router(self.wallet_router)
        self.app.include_router(self.claimed_router)
        self.app.include_router(self.claimed_v2_router)
        self.app.include_router(self.fixed_list_router)
        self.app.include_router(self.fixed_list_v2_router)
        self.app.include_router(self.top_collections_router)
        self.app.include_router(self.dictionary_router)
        self.app.include_router(self.inputs_router)
        self.app.include_router(self.nft_holders_router)

        self.app.include_router(self.metrics_router)

    def register_error_handlers(self) -> None:
        self.app.add_exception_handler(ValueError, value_error_exception_handler)

    def register_middlewares(self) -> None:
        self.app.add_middleware(MetricsMiddleware)

    def get_app(self) -> FastAPI:
        self.include_routers()
        self.register_error_handlers()
        self.register_middlewares()

        return self.app
