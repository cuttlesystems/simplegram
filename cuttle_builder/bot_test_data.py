from typing import List

from b_logic.data_objects import BotMessage, MessageVariant
from cuttle_builder.bot_generator import BotGenerator


class BotTestData:
    _MESSAGES_JSON = [
        {
            'id': 10,
            'text': 'Message 10 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 20,
            'text': 'Message 20 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 30,
            'text': 'Message 30 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 40,
            'text': 'Message 40 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 50,
            'text': 'Message 50 text',
            'photo': None,
            'video': None,
            'file': None
        },
    ]

    _VARIANTS_JSON = [
        {
            'text': 'from 10 to 30',
            'current_id': 10,
            'next_id': 30
        },
        {
            'text': 'From 10 to 20',
            'current_id': 10,
            'next_id': 20
        },
        {
            'text': 'From 10 to 40',
            'current_id': 10,
            'next_id': 40
        },
        {
            'text': 'From 30 to 50',
            'current_id': 30,
            'next_id': 50
        },
        {
            'text': 'From 20 to 50',
            'current_id': 20,
            'next_id': 50
        },
        {
            'text': 'From 50 to 10',
            'current_id': 50,
            'next_id': 10
        }
    ]

    _START_MESSAGE_ID = 10

    _TOKEN = '5689990303:AAEnr1DqNhBvx_zwVt9rnb2P3YJynvjq2rg'

    def __init__(self):
        messages: List[BotMessage] = []
        variants: List[MessageVariant] = []
        for message in self._MESSAGES_JSON:
            mes = BotMessage()
            mes.text = message['text']
            mes.id = message['id']
            messages.append(mes)

        for variant in self._VARIANTS_JSON:
            var = MessageVariant()
            var.text = variant['text']
            var.current_message_id = variant['current_id']
            var.next_message_id = variant['next_id']
            variants.append(var)

        self._messages = messages
        self._variants = variants

    @property
    def start_message_id(self) -> int:
        return 10

    @property
    def messages(self) -> List[BotMessage]:
        return self._messages

    @property
    def variants(self) -> List[MessageVariant]:
        return self._variants

    @property
    def TOKEN(self) -> List[MessageVariant]:
        return self._TOKEN


