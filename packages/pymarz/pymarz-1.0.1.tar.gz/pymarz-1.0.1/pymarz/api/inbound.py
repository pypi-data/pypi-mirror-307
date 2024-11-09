from typing import Dict, List

from .base import BaseAPI
from ..models import (
    HttpMethod,
    Inbound,
)


class InboundAPI(BaseAPI):
    async def get_all(self) -> Dict[str, List[Inbound]]:
        """
        Retrieve inbound configurations grouped by protocol.
        """
        data = await self._client._request(HttpMethod.GET, "/api/inbounds")
        return {key: [Inbound(**item) for item in value] for key, value in data.items()}
