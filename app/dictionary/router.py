from fastapi import APIRouter

from app.dictionary.schemas import GetDictionaryResponse
from app.dictionary.service import DictionaryService


def get_router(dictionary_service: DictionaryService) -> APIRouter:
    router = APIRouter(prefix="/v1/dictionary", tags=["dictionary"])

    @router.get("/")
    async def get() -> GetDictionaryResponse:
        response = await dictionary_service.get_dictionary()
        return response

    return router
