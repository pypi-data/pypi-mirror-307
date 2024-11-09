from typing import Dict, List

from .base import BaseAPI
from ..models import (
    HttpMethod,
    SystemStats,
)


class SystemAPI(BaseAPI):
    async def stats(self) -> SystemStats:
        data = await self._client._request(HttpMethod.GET, "/api/system")
        return SystemStats(**data)
