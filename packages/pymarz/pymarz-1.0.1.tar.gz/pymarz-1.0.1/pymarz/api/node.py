from typing import List
from datetime import datetime

from .base import BaseAPI
from ..models import (
    HttpMethod,
    NodeCreate,
    NodeModify,
    NodeResponse,
    NodeSettings,
    NodeUsageResponse,
    NodesUsageResponse,
)
from ..utils import datetime_to_str


class NodeAPI(BaseAPI):
    async def create(self, data: NodeCreate) -> NodeResponse:
        data = await self._client._request(HttpMethod.POST, "/api/node", data=data)
        return NodeResponse(**data)

    async def update(self, node_id: int, data: NodeModify) -> NodeResponse:
        data = await self._client._request(
            HttpMethod.PUT, f"/api/node/{node_id}", data=data
        )
        return NodeResponse(**data)

    async def delete(self, node_id: int) -> dict:
        data = await self._client._request(HttpMethod.DELETE, f"/api/node/{node_id}")
        return dict(**data)

    async def get(self, node_id: int) -> NodeResponse:
        data = await self._client._request(HttpMethod.GET, f"/api/node/{node_id}")
        return NodeResponse(**data)

    async def get_all(self) -> List[NodeResponse]:
        data = await self._client._request(HttpMethod.GET, f"/api/nodes")
        return [NodeResponse(**node) for node in data]

    async def settings(self) -> NodeSettings:
        data = await self._client._request(HttpMethod.GET, "/api/node/settings")
        return NodeSettings(**data)

    async def reconnect(self, node_id: int) -> dict:
        data = await self._client._request(
            HttpMethod.POST, f"/api/node/{node_id}/reconnect"
        )
        return dict(**data)

    async def usage(
        self,
        start: datetime = None,
        end: datetime = None,
    ) -> NodesUsageResponse:
        params = {
            "start": datetime_to_str(start),
            "end": datetime_to_str(end),
        }
        data = await self._client._request(
            HttpMethod.GET,
            f"/api/nodes/usage",
            params=params,
        )
        return NodesUsageResponse(usages=[NodeUsageResponse(*usage) for usage in data])
