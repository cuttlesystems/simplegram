import copy
import typing
from typing import List

from b_logic.data_objects import HandlerInit, BotDescription, BotCommand, BotMessage, BotVariant, MessageTypeEnum
from cuttle_builder.builder.additional.helpers.find_functions import find_variants_of_message
from cuttle_builder.exceptions.bot_gen_exceptions import NoStartMessageException, NoOneMessageException, TokenException


class DbBotDataPreprocessor:

    def __init__(
            self,
            messages: List[BotMessage],
            variants: List[BotVariant],
            commands: List[BotCommand],
            bot: BotDescription,
            bot_path: str,
    ):
        assert all(isinstance(bot_mes, BotMessage) for bot_mes in messages)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        assert all(isinstance(command, BotCommand) for command in commands)
        assert isinstance(bot, BotDescription)
        assert isinstance(bot_path, str)

        self._messages: List[BotMessage] = copy.deepcopy(messages)
        self._variants: List[BotVariant] = copy.deepcopy(variants)
        self._commands: List[BotCommand] = copy.deepcopy(commands)
        self._token = bot.bot_token
        self._bot = bot
        self._bot_directory = bot_path

    def preprocess_all_data(self):
        if self._is_start_message_id_none(self.bot.start_message_id):
            raise NoStartMessageException(
                'Can\'t generate bot without start message. '
                'Set start message is required.'
            )
        if self._is_messages_empty(self._messages):
            raise NoOneMessageException(
                'Can\'t generate bot without messages. '
                'At least one message is required.')
        if self._is_invalid_token(self._token):
            raise TokenException('Token is invalid!')

        self._remove_next_message_for_variants_with_any_input_message()

    def _remove_next_message_for_variants_with_any_input_message(self):
        for message in self._messages:
            if message.message_type == MessageTypeEnum.ANY_INPUT:
                any_input_variants = find_variants_of_message(message.id, self._variants)
                for variant in any_input_variants:
                    variant.next_message_id = None

    def _is_start_message_id_none(self, start_message_id: typing.Optional[int]):
        if start_message_id is None:
            return True
        return False

    def _is_messages_empty(self, messages: List[BotMessage]):
        if len(messages) == 0:
            return True
        return False

    def _is_invalid_token(self, token: str) -> bool:
        left, sep, right = token.partition(':')
        if (not sep) or (not left.isdigit()) or (not right):
            return True
        return False

    @property
    def messages(self):
        return self._messages

    @property
    def variants(self):
        return self._variants

    @property
    def commands(self):
        return self._commands

    @property
    def token(self):
        return self._token

    @property
    def bot_directory(self):
        return self._bot_directory

    @property
    def bot(self):
        return self._bot

