from typing import List, Optional

from .base import BaseAPI
from ..models import (
    HttpMethod,
    Admin,
    AdminCreate,
    AdminModify,
    Detail,
)


class AdminAPI(BaseAPI):
    async def get_current(self) -> Admin:
        data = await self._client._request(HttpMethod.GET, "/api/admin")
        return Admin(**data)

    async def create(self, data: AdminCreate) -> Admin:
        data = await self._client._request(
            HttpMethod.POST, "/api/admin", data=data
        )
        return Admin(**data)

    async def update(self, username: str, data: AdminModify) -> Admin:
        data = await self._client._request(
            HttpMethod.PUT, f"/api/admin/{username}", data=data
        )
        return Admin(**data)

    async def delete(self, username: str) -> Detail:
        data = await self._client._request(HttpMethod.DELETE, f"/api/admin/{username}")
        return Detail(**data)

    async def get_all(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        username: Optional[str] = None,
    ) -> List[Admin]:
        params = {"offset": offset, "limit": limit, "username": username}
        data = await self._client._request(HttpMethod.GET, "/api/admins", params=params)
        return [Admin(**admin_data) for admin_data in data]
