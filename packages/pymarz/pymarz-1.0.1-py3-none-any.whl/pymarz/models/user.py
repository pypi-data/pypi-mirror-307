from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pymarz.models.admin import Admin
from pymarz.models.base import BaseModel
from pymarz.models.proxy import ProxyTypes


class ReminderType(str, Enum):
    EXPIRATION_DATE = "expiration_date"
    DATA_USAGE = "data_usage"


class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LIMITED = "limited"
    EXPIRED = "expired"
    ON_HOLD = "on_hold"


class UserStatusModify(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    ON_HOLD = "on_hold"


class UserStatusCreate(str, Enum):
    ACTIVE = "active"
    ON_HOLD = "on_hold"


class UserDataLimitResetStrategy(str, Enum):
    NO_REST = "no_reset"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class ClientType(str, Enum):
    SING_BOX = "sing-box"
    CLASH_META = "clash-meta"
    CLASH = "clash"
    OUTLINE = "outline"
    V2RAY = "v2ray"
    V2RAY_JSON = "v2ray-json"


@dataclass
class User(BaseModel):
    proxies: Dict[ProxyTypes, Dict]
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    inbounds: Dict[ProxyTypes, List[str]] = None
    note: Optional[str] = None
    on_hold_timeout: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    auto_delete_in_days: Optional[int] = None


@dataclass
class UserCreate(BaseModel):
    username: str
    proxies: Dict[ProxyTypes, Dict]
    status: UserStatusCreate = None
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    inbounds: Dict[ProxyTypes, List[str]] = None
    note: Optional[str] = None
    on_hold_timeout: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    auto_delete_in_days: Optional[int] = None


@dataclass
class UserModify(BaseModel):
    proxies: Dict[ProxyTypes, Dict]
    status: UserStatusModify = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    inbounds: Dict[ProxyTypes, List[str]] = None
    note: Optional[str] = None
    on_hold_timeout: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    auto_delete_in_days: Optional[int] = None


@dataclass
class UserResponse(BaseModel):
    username: str
    status: UserStatus
    used_traffic: int
    created_at: datetime
    proxies: Dict[ProxyTypes, Dict]
    lifetime_used_traffic: int = 0
    links: List[str] = None
    subscription_url: str = ""
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    inbounds: Dict[ProxyTypes, List[str]] = None
    note: Optional[str] = None
    on_hold_timeout: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    auto_delete_in_days: Optional[int] = None
    sub_updated_at: Optional[datetime] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
    excluded_inbounds: Optional[str] = None
    admin: Optional[Admin] = None


@dataclass
class UsersResponse(BaseModel):
    users: List[UserResponse]
    total: int


@dataclass
class UserUsageResponse(BaseModel):
    node_id: Union[int, None]
    node_name: str
    used_traffic: int


@dataclass
class UserUsagesResponse(BaseModel):
    username: str
    usages: List[UserUsageResponse]


@dataclass
class UsersUsagesResponse(BaseModel):
    usages: List[UserUsageResponse]


@dataclass
class SubscriptionUserResponse(BaseModel):
    username: str
    status: UserStatus
    used_traffic: int
    created_at: datetime
    proxies: Dict[ProxyTypes, Dict]
    lifetime_used_traffic: int = 0
    links: List[str] = None
    subscription_url: str = ""
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: Optional[UserDataLimitResetStrategy] = None
    inbounds: Dict[ProxyTypes, List[str]] = None
    note: Optional[str] = None
    on_hold_timeout: Optional[str] = None
    on_hold_expire_duration: Optional[int] = None
    auto_delete_in_days: Optional[int] = None
    sub_updated_at: Optional[datetime] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
