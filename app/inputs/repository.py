from typing import List, Type

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.inputs.mapper import ActivityMetadataMapper
from app.inputs.models import ActivityMetadata
from app.inputs.schemas import ActivityMetadataItem


class ActivityMetadataRepository:
    session: async_sessionmaker[AsyncSession]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        item_mapper: Type[ActivityMetadataMapper] = ActivityMetadataMapper,
    ):
        self.session = session
        self.item_mapper = item_mapper

    async def fetch_activity_metadatas(
        self,
    ) -> List[ActivityMetadataItem]:
        query = (
            sa.select(ActivityMetadata)
            .select_from(ActivityMetadata)
            .order_by(ActivityMetadata.address)
        )
        async with self.session() as session:
            rows = await session.execute(query)

        items = self.item_mapper.map_to_activity_metadata_items(rows)

        return items
