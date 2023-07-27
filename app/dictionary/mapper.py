from typing import Any, List, Tuple

import sqlalchemy as sa

from app.dictionary.enums import DictionaryValueType
from app.dictionary.models import DictionaryItem
from app.dictionary.schemas import Dictionary, KVItem


class DictionaryMapper:
    @classmethod
    def _convert_dictionary_value_type(
        cls, value: str, value_type: DictionaryValueType
    ) -> Any:
        if value_type == DictionaryValueType.INTEGER:
            return int(value)
        else:
            raise ValueError(f'Unknown value type: {value_type}')

    @classmethod
    def map_to_dictionary(cls, items: List[KVItem]) -> Dictionary:
        values = {
            item.key: cls._convert_dictionary_value_type(item.value, item.value_type)
            for item in items
        }
        return Dictionary(
            eth_price_usd=values.get('eth_price_usd'),
            last_block_timestamp=values.get('last_block_timestamp'),
        )

    @classmethod
    def map_to_dictionary_items(
        self, rows: sa.Result[Tuple[DictionaryItem]]
    ) -> List[KVItem]:
        return [
            KVItem(
                key=row.DictionaryItem.key,
                value=row.DictionaryItem.value,
                value_type=row.DictionaryItem.value_type,
                updated=row.DictionaryItem.updated.timestamp(),
            )
            for row in rows
        ]
