from dataclasses import dataclass
from typing import Optional

from .base import BaseModel


@dataclass
class Default(BaseModel):
    success: Optional[bool] = None
    message: Optional[str] = None


@dataclass
class Detail(BaseModel):
    detail: Optional[str] = None
