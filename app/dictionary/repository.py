from typing import List, Type

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.dictionary.mapper import DictionaryMapper
from app.dictionary.models import DictionaryItem
from app.dictionary.schemas import KVItem


class DictionaryRepository:
    session: async_sessionmaker[AsyncSession]
    item_mapper: Type[DictionaryMapper]

    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        item_mapper: Type[DictionaryMapper] = DictionaryMapper,
    ):
        self.session = session
        self.item_mapper = item_mapper

    async def fetch_dictionary(
        self,
    ) -> List[KVItem]:
        query = (
            sa.select(DictionaryItem)
            .select_from(DictionaryItem)
            .order_by(DictionaryItem.key)
        )
        async with self.session() as session:
            rows = await session.execute(query)

        items = self.item_mapper.map_to_dictionary_items(rows)

        return items
