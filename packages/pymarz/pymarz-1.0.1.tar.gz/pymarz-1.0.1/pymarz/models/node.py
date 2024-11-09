from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .base import BaseModel


class NodeStatus(str, Enum):
    CONNECTED = "connected"
    CONNECTING = "connecting"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class NodeSettings(BaseModel):
    min_node_version: str
    certificate: str


@dataclass
class Node(BaseModel):
    name: str
    address: str
    usage_coefficient: float
    port: int = 62050
    api_port: int = 62051


@dataclass
class NodeCreate(BaseModel):
    name: str
    address: str
    usage_coefficient: float
    add_as_new_host: bool
    port: int = 62050
    api_port: int = 62051


@dataclass
class NodeModify(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    api_port: Optional[int] = None
    status: Optional[NodeStatus] = None
    usage_coefficient: Optional[float] = None


@dataclass
class NodeResponse(BaseModel):
    id: int
    name: str
    address: str
    port: int
    api_port: int
    usage_coefficient: float
    status: NodeStatus
    xray_version: Optional[str] = None
    message: Optional[str] = None


@dataclass
class NodeUsageResponse(BaseModel):
    node_name: str
    uplink: int
    downlink: int
    node_id: Optional[int] = None


@dataclass
class NodesUsageResponse(BaseModel):
    usages: List[NodeUsageResponse]
