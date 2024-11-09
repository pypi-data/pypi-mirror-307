import json
import requests
from typing import Dict

from asgiref.sync import sync_to_async


from ..models import (
    HttpMethod,
    Token,
)


class ClientAPI:
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        timeout: int = 30,
    ):
        self.url = url
        self.timeout = timeout
        self.username = username
        self.password = password

    async def _get_auth_header(self) -> Dict[str, str]:
        try:
            getattr(self, "_token")
        except AttributeError:
            self._token = await self._fetch_new_token(self.username, self.password)

        return {"Authorization": f"{self._token.token_type} {self._token.access_token}"}

    async def _fetch_new_token(self, username: str, password: str) -> Token:
        auth_data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        res = await sync_to_async(requests.post)(
            f"{self.url}/api/admin/token", data=auth_data, timeout=self.timeout
        )
        res.raise_for_status()
        return Token(**res.json())

    async def _request(
        self,
        method: HttpMethod,
        endpoint: str,
        data=None,
        params=None,
        header=None,
        retry: bool = True,
    ):
        url = f"{self.url}{endpoint}"

        if data:
            if type(data) == dict:
                data = json.dumps(data)
            else:
                data = data.to_json()

        headers = await self._get_auth_header()
        if header:
            headers.update(header)

        res = await sync_to_async(requests.request)(
            method.value,
            url,
            params=params,
            headers=headers,
            data=data,
            timeout=self.timeout,
        )

        if res.status_code == 401 and retry:
            await self.login()
            headers = await self._get_auth_header()
            if header:
                headers.update(header)

            res = await sync_to_async(requests.request)(
                method.value,
                url,
                params=params,
                headers=headers,
                data=data,
                timeout=self.timeout,
            )

        res.raise_for_status()
        return res.json()

    async def login(self, username: str = None, password: str = None) -> Token:
        self.username = username or self.username
        self.password = password or self.password

        self._token = await self._fetch_new_token(username, password)
        return self._token


class BaseAPI:
    def __init__(self, client: ClientAPI) -> None:
        self._client = client
