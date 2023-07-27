import csv
import io
from typing import Any, Callable, Coroutine, List, Tuple, TypeVar, Union

from app.audience.schemas import AudienceCSVExportRequest, AudienceItem
from app.claimed.schemas import ClaimedCSVExportRequest, ClaimedItem
from app.common.cloud_storage import CloudStorageService
from app.common.helpers import export_item_attrs_to_csv
from app.common.schemas import AudienceCSVExportResponse
from app.fixed_list.schemas import FixedCSVExportRequest, FixedListItem

T = TypeVar(
    "T", AudienceCSVExportRequest, ClaimedCSVExportRequest, FixedCSVExportRequest
)


class ExportService:
    cloud_storage_service: CloudStorageService

    def __init__(
        self,
        cloud_storage_service: CloudStorageService,
    ):
        self.cloud_storage_service = cloud_storage_service

    async def makeAudienceExport(
        self,
        request: T,
        fetcher: Callable[
            [T],
            Coroutine[
                Any,
                Any,
                Tuple[
                    Union[List[AudienceItem], List[ClaimedItem], List[FixedListItem]],
                    bool,
                ],
            ],
        ],
    ) -> AudienceCSVExportResponse:
        output = io.StringIO()
        csvFile = csv.writer(
            output,
            quoting=csv.QUOTE_MINIMAL,
        )

        # Fill first header row
        csvFile.writerow(list(map(lambda make: make.nice_name, request.fields)))

        # Iterate by batches to prevent enormous RAM usage
        has_next = True
        left_limit = request.limit or 1000
        offset = 0
        request.limit = min(left_limit, 10_000)  # batch size
        is_empty_file = True

        while has_next and left_limit > 0:
            audience, next = await fetcher(request)

            has_next = next
            left_limit = left_limit - request.limit
            offset += request.limit
            request.offset = offset

            for item in audience:
                csvFile.writerow(export_item_attrs_to_csv(item, request.fields))
                if is_empty_file:
                    is_empty_file = False

        if is_empty_file:
            return AudienceCSVExportResponse(uploaded_file_url=None)

        file_name_with_path = f'audience/{request.file_name}'

        uploaded_file_url = await self.cloud_storage_service.async_upload_string(
            file_string=output.getvalue(),
            file_path=file_name_with_path,
            file_name=request.file_name,
        )

        return AudienceCSVExportResponse(uploaded_file_url=uploaded_file_url)
