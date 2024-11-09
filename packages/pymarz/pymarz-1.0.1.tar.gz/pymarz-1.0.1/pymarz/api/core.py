from .base import BaseAPI
from ..models import HttpMethod, CoreStats


class CoreAPI(BaseAPI):
    async def stats(self) -> CoreStats:
        data = await self._client._request(HttpMethod.GET, "/api/core")
        return CoreStats(**data)

    async def restart(self) -> dict:
        return await self._client._request(HttpMethod.POST, "/api/core/restart")
