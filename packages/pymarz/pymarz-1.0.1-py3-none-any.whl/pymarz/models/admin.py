from dataclasses import dataclass
from typing import Optional

from .base import BaseModel


@dataclass
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@dataclass
class Admin(BaseModel):
    username: str
    is_sudo: bool
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None


@dataclass
class AdminCreate(BaseModel):
    username: str
    is_sudo: bool
    password: str
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None


@dataclass
class AdminModify(BaseModel):
    is_sudo: bool
    password: Optional[str] = None
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None
