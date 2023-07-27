from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient


from app.healthcheck.router import get_router
from app.healthcheck.service import HealthCheckService


@pytest.fixture
def healthcheck_service():
    return AsyncMock(spec=HealthCheckService)


@pytest.mark.asyncio
async def test_health(healthcheck_service):
    # Setup the mock to return a specific value
    healthcheck_service.health.return_value = {"status": "ok", "db": "ok"}

    # Create a TestClient instance
    client = TestClient(get_router(healthcheck_service))

    # Send a GET request to the /healthcheck endpoint
    response = client.get("/healthcheck/")

    # # Check that the response status code is 200 OK
    assert response.status_code == 200

    # # Check that the response body is correct
    assert response.json() == {"status": "ok", "db": "ok"}
