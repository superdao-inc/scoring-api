from typing import List, Tuple

import sqlalchemy as sa

from app.inputs.models import ActivityMetadata
from app.inputs.schemas import ActivityMetadataItem


class ActivityMetadataMapper:
    @classmethod
    def map_to_activity_metadata_items(
        cls, rows: sa.Result[Tuple[ActivityMetadata]]
    ) -> List[ActivityMetadataItem]:
        return [
            ActivityMetadataItem(
                address=row.ActivityMetadata.address,
                chain=row.ActivityMetadata.chain,
                name=row.ActivityMetadata.name,
                external_url=row.ActivityMetadata.external_url,
                image_url=row.ActivityMetadata.image_url,
            )
            for row in rows
        ]
