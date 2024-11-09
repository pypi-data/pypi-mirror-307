from datetime import datetime


from .base import BaseAPI
from ..models import (
    HttpMethod,
    ClientType,
    SubscriptionUserResponse,
)
from ..utils import datetime_to_str


class SubscriptionAPI(BaseAPI):
    async def get(self, token: str, user_agent: str = None) -> dict:
        data = await self._client._request(
            HttpMethod.GET,
            f"/sub/{token}/",
            header={"user-agent": user_agent} if user_agent else None,
        )
        return dict(**data)

    async def get_with_client_type(
        self, token: str, client: ClientType = ClientType.V2RAY, user_agent: str = None
    ) -> dict:
        data = await self._client._request(
            HttpMethod.GET,
            f"/sub/{token}/{client.value}",
            header={"user-agent": user_agent} if user_agent else None,
        )
        return dict(**data)

    async def info(self, token: str) -> SubscriptionUserResponse:
        data = await self._client._request(HttpMethod.GET, f"/sub/{token}/info")
        return SubscriptionUserResponse(**data)

    async def usage(
        self, token: str, start: datetime = None, end: datetime = None
    ) -> dict:
        params = {
            "start": datetime_to_str(start),
            "end": datetime_to_str(end),
        }
        data = await self._client._request(
            HttpMethod.GET,
            f"/sub/{token}/usage",
            params=params,
        )
        return dict(**data)
