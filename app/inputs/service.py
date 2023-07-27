from app.inputs.repository import ActivityMetadataRepository
from app.inputs.schemas import GetActivityMetadataResponse


class InputsService:
    activity_metadata_repository: ActivityMetadataRepository

    def __init__(self, activity_metadata_repository: ActivityMetadataRepository):
        self.activity_metadata_repository = activity_metadata_repository

    async def get_activity_metadatas(self) -> GetActivityMetadataResponse:
        items = await self.activity_metadata_repository.fetch_activity_metadatas()
        return GetActivityMetadataResponse(items=items)
