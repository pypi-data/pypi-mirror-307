from dataclasses import dataclass

from .base import BaseModel


@dataclass
class CoreStats(BaseModel):
    version: str
    started: bool
    logs_websocket: str
