import datetime
from unittest.mock import MagicMock
import pytest

from app.dictionary.enums import DictionaryValueType
from app.dictionary.models import DictionaryItem
from app.dictionary.mapper import DictionaryMapper
from app.dictionary.schemas import KVItem, Dictionary


@pytest.fixture
def mapper():
    return DictionaryMapper


@pytest.fixture
def dictionary_objects():
    return [
        MagicMock(
            DictionaryItem=DictionaryItem(
                key='eth_price_usd',
                value='100',
                value_type=DictionaryValueType.INTEGER,
                updated=datetime.datetime(2022, 2, 22, 22, 22, 22),
            )
        ),
        MagicMock(
            DictionaryItem=DictionaryItem(
                key='last_block_timestamp',
                value='1600000042',
                value_type=DictionaryValueType.INTEGER,
                updated=datetime.datetime(2011, 1, 11, 11, 11, 11),
            )
        ),
    ]


def test_map_to_dictionary_items(mapper, dictionary_objects):
    items = mapper.map_to_dictionary_items(dictionary_objects)

    assert all(isinstance(item, KVItem) for item in items)

    assert items == [
        KVItem(
            key='eth_price_usd',
            value='100',
            value_type=DictionaryValueType.INTEGER,
            updated=datetime.datetime(2022, 2, 22, 22, 22, 22).timestamp(),
        ),
        KVItem(
            key='last_block_timestamp',
            value='1600000042',
            value_type=DictionaryValueType.INTEGER,
            updated=datetime.datetime(2011, 1, 11, 11, 11, 11).timestamp(),
        ),
    ]


def test_map_to_dictionary(mapper, dictionary_objects):
    items = mapper.map_to_dictionary_items(dictionary_objects)
    dictionary = mapper.map_to_dictionary(items)

    assert dictionary == Dictionary(eth_price_usd=100, last_block_timestamp=1600000042)


def test_map_to_dictionary_empty(mapper):
    dictionary = mapper.map_to_dictionary([])

    assert dictionary == Dictionary()
