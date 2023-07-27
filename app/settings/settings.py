from typing import Literal, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    mode: Literal["dev", "prod", "stage", "test"] = "dev"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_password: str = "postgres"
    test_db_name: str = "test_postgres"
    sentry_dsn: Optional[str] = None
    prometheus_multiproc_dir: Optional[str] = None
    google_storage_credentials: Optional[str] = None

    similar_wallets_api_url: str = ""

    class Config:
        # `.env.prod` takes priority over `.env`
        env_file = '.env', '.env.prod'
