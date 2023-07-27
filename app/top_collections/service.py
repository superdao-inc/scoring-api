from app.top_collections.models import TopCollectionsBaseModel
from app.top_collections.repository import TopCollectionsRepository
from app.top_collections.schemas import (
    TopCollectionsItem,
    TopCollectionsQuery,
    TopCollectionsResponse,
)


class TopCollectionsService:
    repository: TopCollectionsRepository

    def __init__(self, repository: TopCollectionsRepository):
        self.repository = repository

    async def get_top_collections(
        self, query: TopCollectionsQuery
    ) -> TopCollectionsResponse:
        result = await self.repository.get_top_collections(
            query.audience_id,
            query.audience_type,
            query.blockchain,
            query.top_n,
            query.order_by_fields,
            query.order_by_direction,
            query.use_whitelisted_activities,
        )

        items = [*map(self._map_model_to_schema_item, result)]

        return TopCollectionsResponse(items=items)

    def _map_model_to_schema_item(
        self, model: TopCollectionsBaseModel
    ) -> TopCollectionsItem:
        return TopCollectionsItem(
            audience_id=model.audience_slug,  # type: ignore
            audience_type=model.audience_type,  # type: ignore
            blockchain=model.chain,  # type: ignore
            contract_address=model.token_address,  # type: ignore
            nfts_count=model.nft_count,  # type: ignore
            holders_count=model.holders_count,  # type: ignore
            total_nfts_count=model.total_nft_count if model.total_nft_count else 0,
            total_holders_count=model.total_holders_count
            if model.total_holders_count
            else 0,
            updated=model.updated.timestamp(),  # type: ignore
        )
