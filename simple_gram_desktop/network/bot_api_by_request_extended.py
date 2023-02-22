from typing import List, Optional

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.bot_api.i_bot_api import SignUpException, UserAuthenticationException, \
    CreatingBotException, GetBotListException, ChangingBotException, DeletingBotException, \
    SettingBotStartMessageException, SettingBotErrorMessageException, GettingBotMessagesException, \
    CreatingMessageException, GettingMessageInformationException, EditingMessageException, DeletingMessageException, \
    DeletingImageException, GettingMessagesVariantsListException, CreatingVariantException, EditingVariantException, \
    LinkingVariantWithNextMessageException, DeletingVariantException, GettingBotCommandsException, \
    CreatingCommandException, BotGenerationException, BotStartupException, BotStopException, \
    GettingRunningBotsInfoException, ReceivingBotLogsException, ConnectionException, DeletingVideoException
from b_logic.data_objects import BotDescription, BotMessage, ButtonTypesEnum, BotVariant, BotCommand, BotLogs
from common.localisation import tran
# from network.bot_api_by_requests import BotApiByRequests


class BotApiMessageException(Exception):
    def __init__(self, mes: str):
        super().__init__(mes)


class BotApiByRequestsProxy(BotApiByRequests):

    def sign_up(self, username: str, email: str, password: str) -> None:
        try:
            super().sign_up(username, email, password)
        except SignUpException as e:
            raise BotApiMessageException(self._tr('Sign up error: {0}').format(e.response.text))
        except ConnectionException as e:
            raise BotApiMessageException(self._tr('Connection error: {0}').format(e.mes))

    def authentication(self, username: str, password: str) -> None:
        try:
            super().authentication(username, password)
        except UserAuthenticationException as e:
            raise BotApiMessageException(self._tr('User authentication error: {0}').format(e.response.text))
        except ConnectionException as e:
            raise BotApiMessageException(self._tr('Connection error: {0}').format(e.mes))

    def get_bots(self) -> List[BotDescription]:
        try:
            return super().get_bots()
        except GetBotListException as e:
            raise BotApiMessageException(self._tr('Getting bot list error: {0}').format(e.response.text))

    def create_bot(self, bot_name: str, bot_token: str, bot_description: str) -> BotDescription:
        try:
            return super().create_bot(bot_name, bot_token, bot_description)
        except CreatingBotException as e:
            raise BotApiMessageException(self._tr('Creating bot error: {0}').format(e.response.text))

    def get_bot_by_id(self, bot_id: int, with_link: int = 0) -> BotDescription:
        try:
            return super().get_bot_by_id(bot_id, with_link)
        except GetBotListException as e:
            raise BotApiMessageException(self._tr('Getting bot list error: {0}').format(e.response.text))

    def change_bot(self, bot: BotDescription) -> None:
        try:
            super().change_bot(bot)
        except ChangingBotException as e:
            raise BotApiMessageException(self._tr('Changing bot error: {0}').format(e.response.text))

    def delete_bot(self, bot_id: int) -> None:
        try:
            super().delete_bot(bot_id)
        except DeletingBotException as e:
            raise BotApiMessageException(self._tr('Deleting bot error: {0}').format(e.response.text))

    def set_bot_start_message(self, bot: BotDescription, start_message: BotMessage) -> None:
        try:
            super().set_bot_start_message(bot, start_message)
        except SettingBotStartMessageException as e:
            raise BotApiMessageException(self._tr('Setting bot start message error: {0}').format(e.response.text))

    def set_bot_error_message(self, bot: BotDescription, error_message: BotMessage) -> None:
        try:
            super().set_bot_error_message(bot, error_message)
        except SettingBotErrorMessageException as e:
            raise BotApiMessageException(self._tr('Setting bot error message error: {0}').format(
                e.response.text))

    def get_messages(self, bot: BotDescription) -> List[BotMessage]:
        try:
            return super().get_messages(bot)
        except GettingBotMessagesException as e:
            raise BotApiMessageException(self._tr('Getting bot messages error: {0}').format(e.response.text))

    def create_message(self, bot: BotDescription, text: str,
                       keyboard_type: ButtonTypesEnum, x: int, y: int,
                       photo: Optional[str] = None,
                       photo_filename: Optional[str] = None) -> BotMessage:
        try:
            return super().create_message(bot, text, keyboard_type, x, y, photo, photo_filename)
        except CreatingMessageException as e:
            raise BotApiMessageException(self._tr('Creating message error: {0}').format(e.response.text))

    def get_one_message(self, message_id: int) -> BotMessage:
        try:
            return super().get_one_message(message_id)
        except GettingMessageInformationException as e:
            raise BotApiMessageException(
                'Getting message information error: {0}'.format(e.response.text))

    def change_message(self, message: BotMessage) -> None:
        try:
            super().change_message(message)
        except EditingMessageException as e:
            raise BotApiMessageException(
                self._tr('Editing message error: {0}').format(e.response.text))

    def remove_message_image(self, message: BotMessage) -> None:
        try:
            super().remove_message_image(message)
        except DeletingImageException as e:
            raise BotApiMessageException(
                self._tr('Deleting image error: {0}').format(e.response.text))

    def remove_message_video(self, message: BotMessage) -> None:
        try:
            super().remove_message_video(message)
        except DeletingVideoException as e:
            raise BotApiMessageException(
                self._tr('Deleting video error: {0}').format(e.response.text))

    def delete_message(self, message: BotMessage):
        try:
            super().delete_message(message)
        except DeletingMessageException as e:
            raise BotApiMessageException(self._tr('Deleting message error: {0}').format(e.response.text))

    def get_variants(self, message: BotMessage) -> List[BotVariant]:
        try:
            return super().get_variants(message)
        except GettingMessagesVariantsListException as e:
            raise BotApiMessageException(
                self._tr('Getting variants list for message error: {0}').format(e.response.text))

    def create_variant(self, message: BotMessage, text: str) -> BotVariant:
        try:
            return super().create_variant(message, text)
        except CreatingVariantException as e:
            raise BotApiMessageException(self._tr('Creating variant error: {0}').format(e.response.text))

    def change_variant(self, variant: BotVariant) -> None:
        try:
            super().change_variant(variant)
        except EditingVariantException as e:
            raise BotApiMessageException(self._tr('Editing variant error: {0}').format(e.response.text))

    def connect_variant(self, variant: BotVariant, message: BotMessage) -> None:
        try:
            super().connect_variant(variant, message)
        except LinkingVariantWithNextMessageException as e:
            raise BotApiMessageException(
                self._tr('Linking variant with next message error: {0}').format(e.response.text))

    def delete_variant(self, variant: BotVariant) -> None:
        try:
            super().delete_variant(variant)
        except DeletingVariantException as e:
            raise BotApiMessageException(self._tr('Deleting variant error: {0}').format(e.response.text))

    def get_commands(self, bot: BotDescription) -> List[BotCommand]:
        try:
            return super().get_commands(bot)
        except GettingBotCommandsException as e:
            raise BotApiMessageException(self._tr('Getting bot commands error: {0}').format(e.response.text))

    def create_command(self, bot: BotDescription, command: str,
                       description: str) -> BotCommand:
        try:
            return super().create_command(bot, command, description)
        except CreatingCommandException as e:
            raise BotApiMessageException(self._tr('Creating command error: {0}').format(e.response.text))

    def generate_bot(self, bot: BotDescription) -> None:
        try:
            super().generate_bot(bot)
        except BotGenerationException as e:
            raise BotApiMessageException(
                self._tr('Bot generation error: {0}').format(e.response.text))

    def start_bot(self, bot: BotDescription) -> None:
        try:
            super().start_bot(bot)
        except BotStartupException as e:
            raise BotApiMessageException(
                self._tr('Bot startup error: {0}').format(e.response.text))

    def stop_bot(self, bot: BotDescription) -> None:
        try:
            super().stop_bot(bot)
        except BotStopException as e:
            raise BotApiMessageException(
                self._tr('Bot stop error: {0}').format(e.response.text))

    def get_running_bots_info(self) -> List[int]:
        try:
            return super().get_running_bots_info()
        except GettingRunningBotsInfoException as e:
            raise BotApiMessageException(
                self._tr('Getting running bots info error: {0}').format(e.response.text))

    def get_bot_logs(self, bot: BotDescription) -> BotLogs:
        try:
            return super().get_bot_logs(bot)
        except ReceivingBotLogsException as e:
            raise BotApiMessageException(self._tr('Receiving bot logs error: {0}').format(e.response.text))

    def _tr(self, mes: str) -> str:
        return tran('BotApiByRequests.manual', mes)
