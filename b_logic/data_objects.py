from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


@dataclass(slots=True)
class HandlerInit:
    handler_name: str
    is_error_message: bool


class ButtonTypes(Enum):
    INLINE = 'IKB'
    REPLY = 'RKB'


@dataclass
class BotDescription:
    id: Optional[int] = None
    bot_name: Optional[str] = None
    bot_token: Optional[str] = None
    bot_description: Optional[str] = None

    _start_message_id: Optional[int] = None

    @property
    def start_message_id(self) -> Optional[int]:
        return self._start_message_id

    @start_message_id.setter
    def start_message_id(self, value: Optional[int]):
        assert isinstance(value, Optional[int])
        self._start_message_id = value


@dataclass
class BotMessage:
    id: Optional[int] = None
    text: Optional[str] = None
    keyboard_type: ButtonTypes = ButtonTypes.REPLY
    photo: Optional[bytes] = None
    photo_filename: Optional[str] = None
    video: Optional[str] = None
    file: Optional[str] = None

    x: Optional[int] = None
    y: Optional[int] = None


@dataclass
class BotVariant:
    id: Optional[int] = None
    text: Optional[str] = None
    current_message_id: Optional[int] = None
    next_message_id: Optional[int] = None


@dataclass
class BotCommand:
    id: Optional[int] = None
    bot_id: Optional[int] = None
    command: Optional[str] = None
    description: Optional[str] = None


@dataclass
class BotLogs:
    stdout_lines: List[str] = field(default_factory=lambda: [])
    stderr_lines: List[str] = field(default_factory=lambda: [])
