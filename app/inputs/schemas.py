from typing import List

from pydantic import BaseModel

from app.common.enums import BlockchainType


class ActivityMetadataItem(BaseModel):
    address: str
    chain: BlockchainType
    name: str
    external_url: str
    image_url: str


class GetActivityMetadataResponse(BaseModel):
    items: List[ActivityMetadataItem]
