from typing import List

from b_logic.data_objects import BotMessage, MessageVariant
from cuttle_builder.bot_generator import BotGenerator


class BotTestData:
    def __init__(self):
        messages_json = [
                {
                    'id': 'message_10',
                    'text': 'Message 10 text',
                    'photo': None,
                    'video': None,
                    'file': None
                },
                {
                    'id': 'message_20',
                    'text': 'Message 20 text',
                    'photo': None,
                    'video': None,
                    'file': None
                },
                {
                    'id': 'message_30',
                    'text': 'Message 30 text',
                    'photo': None,
                    'video': None,
                    'file': None
                },
                {
                    'id': 'message_40',
                    'text': 'Message 40 text',
                    'photo': None,
                    'video': None,
                    'file': None
                },
                {
                    'id': 'message_50',
                    'text': 'Message 50 text',
                    'photo': None,
                    'video': None,
                    'file': None
                },
            ]

        variants_json = [
                {
                    'text': 'from 10 to 30',
                    'current_id': 'message_10',
                    'next_id': 'message_30'
                },
                {
                    'text': 'From 10 to 20',
                    'current_id': 'message_10',
                    'next_id': 'message_20'
                },
                {
                    'text': 'From 10 to 40',
                    'current_id': 'message_10',
                    'next_id': 'message_40'
                },
                {
                    'text': 'From 30 to 50',
                    'current_id': 'message_30',
                    'next_id': 'message_50'
                },
                {
                    'text': 'From 20 to 50',
                    'current_id': 'message_20',
                    'next_id': 'message_50'
                },
                {
                    'text': 'From 50 to 10',
                    'current_id': 'message_50',
                    'next_id': 'message_10'
                }
            ]

        messages: List[BotMessage] = []
        variants: List[MessageVariant] = []
        for message in messages_json:
            mes = BotMessage()
            mes.text = message['text']
            mes.id = message['id']
            messages.append(mes)

        for varinat in variants_json:
            var = MessageVariant()
            var.text = varinat['text']
            var.current_message_id = varinat['current_id']
            var.next_message_id = varinat['next_id']
            variants.append(var)

        self._messages = messages
        self._variants = variants

    @property
    def start_message_id(self) -> str:
        return 'message_10'

    @property
    def messages(self) -> List[BotMessage]:
        return self._messages

    @property
    def variants(self) -> List[MessageVariant]:
        return self._variants


if __name__ == '__main__':
    test_data = BotTestData()
    botGenerator = BotGenerator(
        test_data.messages,
        test_data.variants,
        test_data.start_message_id,
        95)
    botGenerator.create_bot()
