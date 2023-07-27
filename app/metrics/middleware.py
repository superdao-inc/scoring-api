import re
import time
from typing import Any

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.metrics.metrics import REQUEST_LATENCY, RESPONSE_STATUS_COUNT


class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        start_time = time.time()

        path = self.normalize_path(request.url.path)

        response = await call_next(request)
        RESPONSE_STATUS_COUNT.labels(
            code=response.status_code,
            route=path,
        ).inc()

        request_latency = time.time() - start_time
        REQUEST_LATENCY.labels(
            code=response.status_code,
            route=path,
        ).observe(request_latency)

        return response

    def normalize_path(self, path: str) -> str:
        path = re.sub(r"0x[0-9a-fA-F]{40}", "{address}", path)
        path = re.sub(r"(?<=\/audience/)\w+", "{slug}", path)
        path = re.sub(r"(?<=\/fixed_list/)\w+", "{slug}", path)
        path = re.sub(r"(?<=\/analytics/)([\-0-9a-f]+)", "{tracker_id}", path)
        path = re.sub(r"\?.*", "", path)

        return path
