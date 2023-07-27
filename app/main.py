import sentry_sdk
from fastapi import FastAPI

from app.analytics.repository import AnalyticsRepository
from app.analytics.router import get_router as AnalyticsRouter
from app.analytics.service import AnalyticsService
from app.audience.repository import AudienceRepository
from app.audience.router import get_router as AudienceRouter
from app.audience.router import get_router_v2 as AudienceRouterV2
from app.audience.router import get_router_v3 as AudienceRouterV3
from app.audience.service import AudienceService
from app.claimed.repository import ClaimedRepository
from app.claimed.router import get_router as ClaimedRouter
from app.claimed.router import get_router_v2 as ClaimedRouterV2
from app.claimed.service import ClaimedService
from app.common.cloud_storage import CloudStorageService
from app.common.export import ExportService
from app.db import Base, build_sync_engine, create_session
from app.dictionary.repository import DictionaryRepository
from app.dictionary.router import get_router as DictionaryRouter
from app.dictionary.service import DictionaryService
from app.fixed_list.repository import FixedListRepository
from app.fixed_list.router import get_router as FixedListRouter
from app.fixed_list.router import get_router_v2 as FixedListRouterV2
from app.fixed_list.service import FixedListService
from app.healthcheck.router import get_router as HealthCheckRouter
from app.healthcheck.service import HealthCheckService
from app.inputs.repository import ActivityMetadataRepository
from app.inputs.router import get_router as InputsRouter
from app.inputs.service import InputsService
from app.metrics.router import get_router as MetricsRouter
from app.metrics.service import MetricsService
from app.nft_holders.repository import NftHoldersRepository
from app.nft_holders.router import get_router as NftHoldersRouter
from app.nft_holders.service import NftHoldersService
from app.rest.app import RestApp
from app.settings.settings import Settings
from app.top_collections.repository import TopCollectionsRepository
from app.top_collections.router import get_router as TopCollectionsRouter
from app.top_collections.service import TopCollectionsService
from app.wallet.repository import WalletRepository
from app.wallet.router import get_router as WalletRouter
from app.wallet.service import WalletService
from app.wallet.similar_wallets_api import SimilarWalletsApi

settings = Settings()
session = create_session(settings)

similar_wallets_api = SimilarWalletsApi(settings)

sentry_sdk.init(
    dsn=settings.sentry_dsn if settings.mode not in ["dev", "test"] else None,
    environment=settings.mode,
    traces_sample_rate=1.0,
)

cloud_storage_service = CloudStorageService(settings)
export_service = ExportService(cloud_storage_service)

healthcheck_service = HealthCheckService(session)
healthcheck_router = HealthCheckRouter(healthcheck_service)

audience_repository = AudienceRepository(session)
audience_service = AudienceService(audience_repository, export_service)
audience_router = AudienceRouter(audience_service)
audience_v2_router = AudienceRouterV2(audience_service)
audience_v3_router = AudienceRouterV3(audience_service)

analytics_repository = AnalyticsRepository(session)
analytics_service = AnalyticsService(analytics_repository)
analytics_router = AnalyticsRouter(analytics_service)

wallet_repository = WalletRepository(session)
wallet_service = WalletService(wallet_repository, similar_wallets_api)
wallet_router = WalletRouter(wallet_service)

claimed_repository = ClaimedRepository(session)
claimed_service = ClaimedService(claimed_repository, export_service)
claimed_router = ClaimedRouter(claimed_service)
claimed_v2_router = ClaimedRouterV2(claimed_service)

fixed_list_repo = FixedListRepository(session)
fixed_list_service = FixedListService(fixed_list_repo, export_service)
fixed_list_router = FixedListRouter(fixed_list_service)
fixed_list_v2_router = FixedListRouterV2(fixed_list_service)

top_collections_repo = TopCollectionsRepository(session)
top_collections_service = TopCollectionsService(top_collections_repo)
top_collections_router = TopCollectionsRouter(top_collections_service)

dictionary_repository = DictionaryRepository(session)
dictionary_service = DictionaryService(dictionary_repository)
dictionary_router = DictionaryRouter(dictionary_service)

metrics_service = MetricsService(settings)
metrics_router = MetricsRouter(metrics_service)

activity_metadata_repository = ActivityMetadataRepository(session)
inputs_service = InputsService(activity_metadata_repository)
inputs_router = InputsRouter(inputs_service)

nft_holders_repository = NftHoldersRepository(session)
nft_holders_service = NftHoldersService(nft_holders_repository)
nft_holders_router = NftHoldersRouter(nft_holders_service)


if settings.mode == "dev":
    engine = build_sync_engine(settings)
    Base.metadata.create_all(engine)


rest = RestApp(
    settings,
    session,
    FastAPI(),
    healthcheck_router,
    audience_router,
    audience_v2_router,
    audience_v3_router,
    analytics_router,
    wallet_router,
    claimed_router,
    claimed_v2_router,
    fixed_list_router,
    fixed_list_v2_router,
    top_collections_router,
    dictionary_router,
    inputs_router,
    metrics_router,
    nft_holders_router,
).get_app
