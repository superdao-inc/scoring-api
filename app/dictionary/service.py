from typing import Type

from app.dictionary.mapper import DictionaryMapper
from app.dictionary.repository import DictionaryRepository
from app.dictionary.schemas import GetDictionaryResponse


class DictionaryService:
    dictionary_repository: DictionaryRepository
    item_mapper: Type[DictionaryMapper] = DictionaryMapper

    def __init__(self, dictionary_repository: DictionaryRepository):
        self.dictionary_repository = dictionary_repository

    async def get_dictionary(self) -> GetDictionaryResponse:
        items = await self.dictionary_repository.fetch_dictionary()
        dictionary = self.item_mapper.map_to_dictionary(items)

        return GetDictionaryResponse(**dictionary.dict())
