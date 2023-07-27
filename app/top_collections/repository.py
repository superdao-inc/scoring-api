from typing import Any, Iterable, Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.common.enums import AudienceType, BlockchainType
from app.common.helpers import get_model_column
from app.top_collections.models import (
    TopCollectionsBaseModel,
    TopCollectionsModel,
    TopWhitelistedCollectionsModel,
)

DEFAULT_TOP_N = 10
MAX_TOP_N = 1000
DEFAULT_ORDER_BY_FIELD = "holders_count"


class TopCollectionsRepository:
    session: async_sessionmaker[AsyncSession]

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def get_top_collections(
        self,
        audience_id: str,
        audience_type: AudienceType,
        blockchain: Optional[BlockchainType] = None,
        top_n: Optional[int] = DEFAULT_TOP_N,
        order_by_fields: Optional[Any] = None,
        order_by_direction: Optional[str] = None,
        use_whitelisted_activities: Optional[bool] = False,
    ) -> Iterable[TopCollectionsBaseModel]:
        if top_n and top_n > MAX_TOP_N:
            raise ValueError(f"top_n should be less than {MAX_TOP_N}")

        model = (
            TopWhitelistedCollectionsModel
            if use_whitelisted_activities
            else TopCollectionsModel
        )

        query = (
            sa.select(model)
            .where(model.audience_slug == audience_id)
            .where(model.audience_type == audience_type)
            .where(model.chain == blockchain if blockchain else sa.true())
            .limit(top_n)
        )

        if not order_by_fields:
            order_by_fields = [DEFAULT_ORDER_BY_FIELD]

        for order_by_field in order_by_fields:
            column = get_model_column(str(order_by_field), model)
            query = query.order_by(
                sa.asc(column) if order_by_direction == "ASC" else sa.desc(column)
            )
        query = query.order_by(sa.desc(model.token_address))

        async with self.session() as session:
            rows = await session.scalars(query)

        return rows.all()
