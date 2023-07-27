from unittest.mock import AsyncMock
from fastapi import APIRouter, FastAPI
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.rest.app import RestApp
from app.settings.settings import Settings


@pytest.fixture
def settings():
    return AsyncMock(spec=Settings)


@pytest.fixture
def session():
    return AsyncMock(spec=async_sessionmaker)


@pytest.fixture
def app():
    return AsyncMock(spec=FastAPI)


@pytest.fixture
def healthcheck_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def audience_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def audience_router_v2():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def audience_router_v3():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def analytics_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def wallet_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def claimed_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def metrics_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def claimed_router_v2():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def fixed_list_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def fixed_list_router_v2():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def top_collections_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def dictionary_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def inputs_router():
    return AsyncMock(spec=APIRouter)


@pytest.fixture
def nft_holders_router():
    return AsyncMock(spec=APIRouter)


@pytest.mark.asyncio
async def test_get_app(
    settings,
    session,
    app,
    healthcheck_router,
    audience_router,
    audience_router_v2,
    audience_router_v3,
    analytics_router,
    wallet_router,
    claimed_router,
    claimed_router_v2,
    fixed_list_router,
    fixed_list_router_v2,
    top_collections_router,
    dictionary_router,
    inputs_router,
    metrics_router,
    nft_holders_router,
):
    # create RestApp instance
    rest_app = RestApp(
        settings=settings,
        session=session,
        app=app,
        healthcheck_router=healthcheck_router,
        audience_router=audience_router,
        audience_v2_router=audience_router_v2,
        audience_v3_router=audience_router_v3,
        analytics_router=analytics_router,
        wallet_router=wallet_router,
        claimed_router=claimed_router,
        claimed_v2_router=claimed_router_v2,
        fixed_list_router=fixed_list_router,
        fixed_list_v2_router=fixed_list_router_v2,
        top_collections_router=top_collections_router,
        dictionary_router=dictionary_router,
        inputs_router=inputs_router,
        metrics_router=metrics_router,
        nft_holders_router=nft_holders_router,
    )

    # call get_app method to include routers in FastAPI instance
    mocked_app = rest_app.get_app()

    # verify that include_router method was called with the expected routers
    mocked_app.include_router.assert_any_call(healthcheck_router)
    mocked_app.include_router.assert_any_call(audience_router)
    mocked_app.include_router.assert_any_call(analytics_router)
    mocked_app.include_router.assert_any_call(wallet_router)
    mocked_app.include_router.assert_any_call(claimed_router)
    mocked_app.include_router.assert_any_call(metrics_router)
    mocked_app.include_router.assert_any_call(audience_router_v2)
    mocked_app.include_router.assert_any_call(audience_router_v3)
    mocked_app.include_router.assert_any_call(claimed_router_v2)
    mocked_app.include_router.assert_any_call(fixed_list_router)
    mocked_app.include_router.assert_any_call(fixed_list_router_v2)
    mocked_app.include_router.assert_any_call(top_collections_router)
    mocked_app.include_router.assert_any_call(dictionary_router)
    mocked_app.include_router.assert_any_call(inputs_router)
    mocked_app.include_router.assert_any_call(nft_holders_router)
