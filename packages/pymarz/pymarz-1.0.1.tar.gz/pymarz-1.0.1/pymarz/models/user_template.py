from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .base import BaseModel
from .proxy import ProxyTypes


@dataclass
class UserTemplate(BaseModel):
    name: Optional[str] = None
    data_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[ProxyTypes, List[str]]] = field(default_factory={})


@dataclass
class UserTemplateCreate(BaseModel):
    name: Optional[str] = None
    data_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[ProxyTypes, List[str]]] = field(default_factory={})


@dataclass
class UserTemplateModify(BaseModel):
    name: Optional[str] = None
    data_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[ProxyTypes, List[str]]] = field(default_factory={})


@dataclass
class UserTemplateResponse(BaseModel):
    id: int
    name: Optional[str] = None
    data_limit: Optional[int] = None
    expire_duration: Optional[int] = None
    username_prefix: Optional[str] = None
    username_suffix: Optional[str] = None
    inbounds: Optional[Dict[ProxyTypes, List[str]]] = field(default_factory={})
