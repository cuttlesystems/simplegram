from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ButtonTypes(Enum):
    INLINE = 'IKB'
    REPLY = 'RKB'


@dataclass
class BotDescription:
    id: Optional[int] = None
    bot_name: Optional[str] = None
    bot_token: Optional[str] = None
    bot_description: Optional[str] = None
    start_message_id: Optional[int] = None


@dataclass
class BotMessage:
    id: Optional[int] = None
    text: Optional[str] = None

    keyboard_type: ButtonTypes = ButtonTypes.REPLY
    # todo: думаю, тут сделать байтовые поля в
    #  которых хранить байтовое содержимое (надо подумать)
    photo: Optional[bytes] = None
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
