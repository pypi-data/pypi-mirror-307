from typing import Dict, List

from .base import BaseAPI
from ..models import (
    HttpMethod,
    Host,
)


class HostAPI(BaseAPI):
    async def get_all(self) -> Dict[str, List[Host]]:
        """
        Get a list of proxy hosts grouped by inbound tag.
        """
        data = await self._client._request(HttpMethod.GET, "/api/hosts")
        return {key: [Host(**item) for item in value] for key, value in data.items()}

    async def update_all(self, data: Dict[str, List[Host]]) -> Dict[str, List[Host]]:
        """
        Recive a list of proxy hosts grouped by inbound tag and update all.
        """
        data = await self._client._request(HttpMethod.PUT, "/api/hosts", data=data)
        return {key: [Host(**item) for item in value] for key, value in data.items()}
