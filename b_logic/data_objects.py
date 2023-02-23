from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


@dataclass(slots=True)
class HandlerInit:
    handler_name: str
    is_error_message: bool


class ButtonTypesEnum(Enum):
    INLINE = 'IKB'
    REPLY = 'RKB'


class MessageTypeEnum(Enum):
    VARIANTS = 'variants'
    ANY_INPUT = 'any_input'
    GOTO = 'goto'


@dataclass(slots=True)
class StartStopBotState:
    IS_STARTED: bool
    API_RESPONSE: str


@dataclass(slots=True)
class BotDescription:
    id: Optional[int] = None
    bot_name: str = 'Undefined bot name'
    bot_token: str = ''
    bot_description: Optional[str] = None
    _start_message_id: Optional[int] = None
    _error_message_id: Optional[int] = None
    bot_link: Optional[str] = None
    bot_profile_photo: Optional[str] = None
    profile_photo_filename: Optional[str] = None

    @property
    def start_message_id(self) -> Optional[int]:
        return self._start_message_id

    @start_message_id.setter
    def start_message_id(self, value: Optional[int]):
        assert isinstance(value, Optional[int])
        self._start_message_id = value

    @property
    def error_message_id(self) -> Optional[int]:
        return self._error_message_id

    @error_message_id.setter
    def error_message_id(self, value: Optional[int]):
        assert isinstance(value, Optional[int])
        self._error_message_id = value


@dataclass(slots=True)
class BotMessage:
    id: Optional[int] = None
    text: str = ''
    keyboard_type: ButtonTypesEnum = ButtonTypesEnum.REPLY
    photo: Optional[str] = None
    photo_file_format: Optional[str] = None
    photo_filename: Optional[str] = None
    video: Optional[str] = None
    file: Optional[str] = None
    message_type: MessageTypeEnum = MessageTypeEnum.VARIANTS
    next_message_id: Optional[int] = None
    variable: str = ''

    x: Optional[int] = None
    y: Optional[int] = None


@dataclass(slots=True)
class BotVariant:
    id: Optional[int] = None
    text: Optional[str] = None
    current_message_id: Optional[int] = None
    next_message_id: Optional[int] = None


@dataclass(slots=True)
class BotCommand:
    id: Optional[int] = None
    bot_id: Optional[int] = None
    command: Optional[str] = None
    description: Optional[str] = None


@dataclass(slots=True)
class BotLogs:
    stdout_lines: List[str] = field(default_factory=lambda: [])
    stderr_lines: List[str] = field(default_factory=lambda: [])
