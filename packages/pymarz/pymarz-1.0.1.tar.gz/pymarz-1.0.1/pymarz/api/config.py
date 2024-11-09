from .base import BaseAPI
from ..models import HttpMethod, CoreStats


class ConfigAPI(BaseAPI):
    async def get(self) -> dict:
        res = await self._client._request(HttpMethod.GET, "/api/core/config")
        return dict(res)

    async def update(self, data: dict) -> dict:
        data = await self._client._request(
            HttpMethod.PUT, "/api/core/config", data=data
        )
        return data
