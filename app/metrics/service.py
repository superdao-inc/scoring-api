from prometheus_client import REGISTRY, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector

from app.settings.settings import Settings


class MetricsService:
    settings: Settings

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def generate_latest(self) -> bytes:
        if path := self.settings.prometheus_multiproc_dir:
            registry = CollectorRegistry()
            MultiProcessCollector(registry, path)  # type: ignore
        else:
            registry = REGISTRY

        return generate_latest(registry)
