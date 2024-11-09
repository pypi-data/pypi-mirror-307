from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from .xray_api import ShadowsocksMethods, XTLSFlows

from .base import BaseModel


class ProxyTypes(str, Enum):
    VMESS = "vmess"
    VLESS = "vless"
    TROJAN = "trojan"
    SHADOWSOCKS = "shadowsocks"

class ProxyHostSecurity(str, Enum):
    DEFAULT = "inbound_default"
    NONE = "none"
    TLS = "tls"


ProxyHostALPN = Enum(
    "ProxyHostALPN",
    {
        "none": "",
        "h3": "h3",
        "h2": "h2",
        "http/1.1": "http/1.1",
        "h3,h2,http/1.1": "h3,h2,http/1.1",
        "h3,h2": "h3,h2",
        "h2,http/1.1": "h2,http/1.1",
    },
)

ProxyHostFingerprint = Enum(
    "ProxyHostFingerprint",
    {
        "none": "",
        "chrome": "chrome",
        "firefox": "firefox",
        "safari": "safari",
        "ios": "ios",
        "android": "android",
        "edge": "edge",
        "360": "360",
        "qq": "qq",
        "random": "random",
        "randomized": "randomized",
    },
)


class VMessSettings(BaseModel):
    id: Optional[UUID] = None


class VLESSSettings(BaseModel):
    id: Optional[UUID] = None
    flow: XTLSFlows = XTLSFlows.NONE


class TrojanSettings(BaseModel):
    password: str
    flow: XTLSFlows = XTLSFlows.NONE


class ShadowsocksSettings(BaseModel):
    password: Optional[str] = None
    method: ShadowsocksMethods = ShadowsocksMethods.CHACHA20_POLY1305


@dataclass
class Host(BaseModel):
    remark: str
    address: str
    port: Optional[int] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    security: ProxyHostSecurity = ProxyHostSecurity.DEFAULT
    alpn: ProxyHostALPN = ProxyHostALPN.none
    fingerprint: ProxyHostFingerprint = ProxyHostFingerprint.none
    allowinsecure: Union[bool, None] = None
    is_disabled: Union[bool, None] = None
    mux_enable: Union[bool, None] = None
    fragment_setting: Optional[str] = None
    noise_setting: Optional[str] = None
    random_user_agent: Union[bool, None] = None


@dataclass
class Inbound(BaseModel):
    tag: str
    protocol: ProxyTypes
    network: str
    tls: str
    port: Union[int, str]
