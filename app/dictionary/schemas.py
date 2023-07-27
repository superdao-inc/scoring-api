from typing import Optional

from pydantic import BaseModel

from app.dictionary.enums import DictionaryValueType


class KVItem(BaseModel):
    key: str
    value: str
    value_type: DictionaryValueType
    updated: int


class Dictionary(BaseModel):
    eth_price_usd: Optional[int] = None
    last_block_timestamp: Optional[int] = None


class GetDictionaryResponse(Dictionary):
    pass
