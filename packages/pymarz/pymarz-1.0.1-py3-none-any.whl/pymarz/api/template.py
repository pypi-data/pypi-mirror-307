from typing import List

from .base import BaseAPI
from ..models import (
    HttpMethod,
    UserTemplateCreate,
    UserTemplateModify,
    UserTemplateResponse,
)


class TemplateAPI(BaseAPI):
    async def get_all(
        self,
        offset: int = None,
        limit: int = None,
    ) -> List[UserTemplateResponse]:
        params = {
            "offset": offset,
            "limit": limit,
        }
        data = await self._client._request(
            HttpMethod.GET,
            f"/api/user_template",
            params=params,
        )
        return [UserTemplateResponse(**template) for template in data]

    async def get(self, id: int) -> UserTemplateResponse:
        """Get User Template information with id"""
        params = {
            "template_id": id,
        }
        data = await self._client._request(
            HttpMethod.GET,
            f"/api/user_template/{id}",
            params=params,
        )
        return UserTemplateResponse(**data)

    async def create(self, data: UserTemplateCreate) -> UserTemplateResponse:
        """
        Add a new user template

            name can be up to 64 characters
            data_limit must be in bytes and larger or equal to 0
            expire_duration must be in seconds and larger or equat to 0
            inbounds dictionary of protocol:inbound_tags, empty means all inbounds
        """
        data = await self._client._request(
            HttpMethod.POST, "/api/user_template", data=data
        )
        return UserTemplateResponse(**data)

    async def update(self, id: int, data: UserTemplateModify) -> UserTemplateResponse:
        """
        Modify User Template

            name can be up to 64 characters
            data_limit must be in bytes and larger or equal to 0
            expire_duration must be in seconds and larger or equat to 0
            inbounds dictionary of protocol:inbound_tags, empty means all inbounds
        """
        params = {
            "template_id": id,
        }
        data = await self._client._request(
            HttpMethod.PUT,
            f"/api/user_template/{id}",
            params=params,
            data=data,
        )
        return UserTemplateResponse(**data)

    async def delete(
        self,
        id: int,
    ) -> dict:
        """Remove a User Template by its ID"""
        params = {
            "template_id": id,
        }
        data = await self._client._request(
            HttpMethod.DELETE,
            f"/api/user_template/{id}",
            params=params,
        )
        return dict(**data)
