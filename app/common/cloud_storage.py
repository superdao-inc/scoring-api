import base64
import json
import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from google.cloud.storage import Client  # type: ignore
from starlette.concurrency import run_in_threadpool

from app.settings.settings import Settings


class CloudStorageService:
    settings: Settings
    bucket_name: str

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        if settings.google_storage_credentials is None:
            logging.warning(
                '[CloudStorageService] google_storage_credentials is required'
            )
            return

        credentials_json_str = base64.b64decode(
            settings.google_storage_credentials
        ).decode("ascii")

        client = Client.from_service_account_info(
            json.loads(credentials_json_str, strict=False)
        )

        self.bucket_name = (
            'reports.superdao.co'
            if settings.mode == 'prod'
            else 'superdao-reports-stage'
        )

        self.bucket = client.bucket(self.bucket_name)

    def upload_string(self, file_string: str, file_path: str, file_name: str) -> str:
        blob = self.bucket.blob(file_path)
        blob.upload_from_string(data=file_string)

        month_from_now = datetime.now() + relativedelta(months=+1)

        return blob.generate_signed_url(
            scheme='https',
            expiration=month_from_now,
            # Will start auto dowload if response_disposition provided
            response_disposition=f'attachment; filename={file_name}',
        )

    async def async_upload_string(
        self, file_string: str, file_path: str, file_name: str
    ) -> str:
        return await run_in_threadpool(
            self.upload_string, file_string, file_path, file_name
        )
