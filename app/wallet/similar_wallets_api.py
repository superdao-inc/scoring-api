from typing import List, Optional

import httpx

from app.settings.settings import Settings


class SimilarWalletsApi:
    def __init__(self, s: Settings) -> None:
        self.base_url = s.similar_wallets_api_url
        self.http_client = httpx.AsyncClient(base_url=self.base_url, timeout=30)

    async def get_index_similar_wallets(
        self, address: str, n: Optional[int] = 5
    ) -> List[str]:
        response = await self.http_client.get(f"/annoy/{address}?n={n}")
        if response.status_code == 204:
            return []

        data = response.json()
        return data['neighbors']
