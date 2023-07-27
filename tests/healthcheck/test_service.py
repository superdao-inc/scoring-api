import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.healthcheck.service import HealthCheckService


@pytest.fixture
def healthcheck():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    return HealthCheckService(session)


@pytest.mark.asyncio
async def test_health(healthcheck):
    assert await healthcheck.health() == {'status': 'ok', 'db': 'ok'}
