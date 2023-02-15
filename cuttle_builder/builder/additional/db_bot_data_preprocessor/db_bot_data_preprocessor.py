from typing import List

from b_logic.data_objects import HandlerInit, BotDescription, BotCommand, BotMessage, BotVariant, MessageTypeEnum
from cuttle_builder.builder.additional.helpers.find_functions import find_variants_of_message
from cuttle_builder.exceptions.bot_gen_exceptions import NoStartMessageException, NoOneMessageException, TokenException


class DbBotDataPreprocessor:

    def validate_all_data(
            self,
            messages: List[BotMessage],
            variants: List[BotVariant],
            commands: List[BotCommand],
            bot: BotDescription,
            bot_path: str):
        assert all(isinstance(bot_mes, BotMessage) for bot_mes in messages)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        assert all(isinstance(command, BotCommand) for command in commands)
        assert isinstance(bot, BotDescription)
        assert isinstance(bot_path, str)

        if self._is_start_message_id_none(bot.start_message_id):
            raise NoStartMessageException(
                'Can\'t generate bot without start message. '
                'Set start message is required.'
            )
        if self._is_messages_empty(messages):
            raise NoOneMessageException(
                'Can\'t generate bot without messages. '
                'At least one message is required.')
        if self._is_invalid_token(bot.bot_token):
            raise TokenException('Token is invalid!')

        variants = self._remove_next_message_for_variants_with_any_input_message(messages, variants)

        return messages, variants, commands, bot, bot_path

    def _remove_next_message_for_variants_with_any_input_message(self, messages: List[BotMessage], variants: List[BotVariant]):
        for message in messages:
            if message.message_type == MessageTypeEnum.ANY_INPUT:
                any_input_variants = find_variants_of_message(message.id, variants)
                for variant in any_input_variants:
                    variant.next_message_id = None
        return variants


    def _is_start_message_id_none(self, start_message_id: int):
        if start_message_id is None:
            return True
        return False

    def _is_messages_empty(self, messages: List[BotMessage]):
        if not messages:
            return True
        return False

    def _is_invalid_token(self, token: str) -> bool:
        left, sep, right = token.partition(':')
        if (not sep) or (not left.isdigit()) or (not right):
            return True
        return False

