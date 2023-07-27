from typing import List, Optional

from pydantic import BaseModel

from app.common.enums import AudienceType, BlockchainType
from app.common.schemas import QueryOrderableMixin


class TopCollectionsQuery(QueryOrderableMixin):
    audience_id: str
    audience_type: AudienceType
    top_n: Optional[int]
    blockchain: Optional[BlockchainType] = None
    use_whitelisted_activities: Optional[bool] = False


class TopCollectionsItem(BaseModel):
    audience_id: str
    audience_type: AudienceType
    blockchain: BlockchainType
    contract_address: str
    nfts_count: int
    holders_count: int
    total_nfts_count: int
    total_holders_count: int
    updated: int


class TopCollectionsResponse(BaseModel):
    items: List[TopCollectionsItem]
