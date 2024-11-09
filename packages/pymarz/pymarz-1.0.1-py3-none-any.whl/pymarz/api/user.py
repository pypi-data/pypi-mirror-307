from typing import List
from datetime import datetime

from .base import BaseAPI
from ..models import (
    HttpMethod,
    UserCreate,
    UserModify,
    UserResponse,
    UserStatus,
    UserUsageResponse,
    UserUsagesResponse,
    UsersResponse,
    UsersUsagesResponse,
)
from ..utils import datetime_to_str


class UserAPI(BaseAPI):
    async def create(self, data: UserCreate) -> UserResponse:
        """
        Add a new user
            username: 3 to 32 characters, can include a-z, 0-9, and underscores.
            status: User's status, defaults to active. Special rules if on_hold.
            expire: UTC timestamp for account expiration. Use 0 for unlimited.
            data_limit: Max data usage in bytes (e.g., 1073741824 for 1GB). 0 means unlimited.
            data_limit_reset_strategy: Defines how/if data limit resets. no_reset means it never resets.
            proxies: Dictionary of protocol settings (e.g., vmess, vless).
            inbounds: Dictionary of protocol tags to specify inbound connections.
            note: Optional text field for additional user information or notes.
            on_hold_timeout: UTC timestamp when on_hold status should start or end.
            on_hold_expire_duration: Duration (in seconds) for how long the user should stay in on_hold status.
        """
        data = await self._client._request(HttpMethod.POST, "/api/user", data=data)
        return UserResponse(**data)

    async def update(self, username: str, data: UserModify) -> UserResponse:
        """
        Modify an existing user
            username: Cannot be changed. Used to identify the user.
            status: User's new status. Can be 'active', 'disabled', 'on_hold', 'limited', or 'expired'.
            expire: UTC timestamp for new account expiration. Set to 0 for unlimited, null for no change.
            data_limit: New max data usage in bytes (e.g., 1073741824 for 1GB). Set to 0 for unlimited, null for no change.
            data_limit_reset_strategy: New strategy for data limit reset. Options include 'daily', 'weekly', 'monthly', or 'no_reset'.
            proxies: Dictionary of new protocol settings (e.g., vmess, vless). Empty dictionary means no change.
            inbounds: Dictionary of new protocol tags to specify inbound connections. Empty dictionary means no change.
            note: New optional text for additional user information or notes. null means no change.
            on_hold_timeout: New UTC timestamp for when on_hold status should start or end. Only applicable if status is changed to 'on_hold'.
            on_hold_expire_duration: New duration (in seconds) for how long the user should stay in on_hold status. Only applicable if status is changed to 'on_hold'.
            Note: Fields set to null or omitted will not be modified.
        """
        data = await self._client._request(
            HttpMethod.PUT, f"/api/user/{username}", data=data
        )
        return UserResponse(**data)

    async def delete(self, username: str) -> dict:
        """Remove a user"""
        data = await self._client._request(HttpMethod.DELETE, f"/api/user/{username}")
        return dict(**data)

    async def revoke_subscription(self, username: str) -> UserResponse:
        """
        Revoke users subscription (Subscription link and proxies)
        """
        data = await self._client._request(
            HttpMethod.POST, f"/api/user/{username}/revoke_sub"
        )
        return UserResponse(**data)

    async def get(self, username: str) -> UserResponse:
        """Get user information"""
        data = await self._client._request(HttpMethod.GET, f"/api/user/{username}")
        return UserResponse(**data)

    async def get_all(
        self,
        search: str = None,
        offset: int = None,
        limit: int = None,
        status: UserStatus = None,
        sort: str = None,
        usernames: List[str] = [],
        admins: List[str] = [],
    ) -> UsersResponse:
        """
        Get all users
        """
        params = {
            "search": search,
            "offset": offset,
            "limit": limit,
            "status": status,
            "sort": sort,
            "username": usernames,
            "admin": admins,
        }

        data = await self._client._request(
            HttpMethod.GET,
            f"/api/users",
            params=params,
        )
        return UsersResponse(
            total=data["total"],
            users=[UserResponse(**user) for user in data["users"]],
        )

    async def get_usage(
        self,
        username: str,
        start: datetime = None,
        end: datetime = None,
    ) -> UserUsagesResponse:
        """
        Get user usage
        """
        params = {
            "start": datetime_to_str(start),
            "end": datetime_to_str(end),
        }
        data = await self._client._request(
            HttpMethod.POST,
            f"/api/user/{username}/usage",
            params=params,
        )
        return UserUsagesResponse(
            username=data["username"],
            usages=[UserUsageResponse(**usage) for usage in ["usages"]],
        )

    async def get_usage_all(
        self,
        start: datetime = None,
        end: datetime = None,
    ) -> UsersUsagesResponse:
        """
        Get users usage
        """

        params = {"start": datetime_to_str(start), "end": datetime_to_str(end)}
        data = await self._client._request(
            HttpMethod.POST,
            f"/api/users/usage",
            params=params,
        )
        return UsersUsagesResponse(
            usages=[UserUsageResponse(**usage) for usage in data["usages"]]
        )

    async def reset_usage(self, username: str) -> UserResponse:
        """
        Reset user data usage
        """
        data = await self._client._request(
            HttpMethod.POST, f"/api/user/{username}/reset"
        )
        return UserResponse(**data)

    async def reset_usage_all(self) -> dict:
        """
        Reset all users data usage
        """
        data = await self._client._request(HttpMethod.POST, f"/api/users/reset")
        return dict(**data)

    async def set_owner(self, username: str, admin_username: str) -> UserResponse:
        """
        Set a new owner (admin) for a user.
        """
        params = {"admin_username": admin_username}
        data = await self._client._request(
            HttpMethod.PUT,
            f"/api/user/{username}/set-owner",
            params=params,
        )
        return UserResponse(**data)

    async def get_expired(
        self,
        expired_after: datetime = None,
        expired_before: datetime = None,
    ) -> List[str]:
        """
        Get users who have expired within the specified date range.

            expired_after UTC datetime (optional)
            expired_before UTC datetime (optional)
            At least one of expired_after or expired_before must be provided for filtering
            If both are omitted, returns all expired users
        """
        params = {
            "expired_after": datetime_to_str(expired_after),
            "expired_before": datetime_to_str(expired_before),
        }
        data = await self._client._request(
            HttpMethod.PUT,
            f"/api/users/expired",
            params=params,
        )
        return data

    async def delete_expired(
        self,
        expired_after: datetime = None,
        expired_before: datetime = None,
    ) -> List[str]:
        """
        Delete users who have expired within the specified date range.

            expired_after UTC datetime (optional)
            expired_before UTC datetime (optional)
            At least one of expired_after or expired_before must be provided
        """
        params = {
            "expired_after": datetime_to_str(expired_after),
            "expired_before": datetime_to_str(expired_before),
        }
        data = await self._client._request(
            HttpMethod.DELETE,
            f"/api/users/expired",
            params=params,
        )
        return data
