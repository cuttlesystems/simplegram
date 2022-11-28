from dataclasses import dataclass
from typing import Optional


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

    # todo: думаю, тут сделать байтовые поля в
    #  которых хранить байтовое содержимое (надо подумать)
    photo: Optional[str] = None
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
