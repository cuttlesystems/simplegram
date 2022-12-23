from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Settings:
    name: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
