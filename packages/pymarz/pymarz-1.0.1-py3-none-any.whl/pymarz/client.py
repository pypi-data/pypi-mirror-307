from .api import (
    ClientAPI,
    AdminAPI,
    ConfigAPI,
    CoreAPI,
    HostAPI,
    InboundAPI,
    NodeAPI,
    SubscriptionAPI,
    SystemAPI,
    TemplateAPI,
    UserAPI,
)


class MarzAPI:
    def __init__(
        self, url: str, username: str, password: str, timeout: int = 30
    ) -> None:
        self._client = ClientAPI(
            url=url,
            username=username,
            password=password,
            timeout=timeout,
        )
        self.admin = AdminAPI(self._client)
        self.config = ConfigAPI(self._client)
        self.core = CoreAPI(self._client)
        self.host = HostAPI(self._client)
        self.inbound = InboundAPI(self._client)
        self.node = NodeAPI(self._client)
        self.subscription = SubscriptionAPI(self._client)
        self.system = SystemAPI(self._client)
        self.template = TemplateAPI(self._client)
        self.user = UserAPI(self._client)

    async def login(self, username: str = None, password: str = None) -> None:
        await self._client.login(username, password)
