from pathlib import Path
from typing import List, Optional
from io import BufferedIOBase

from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.conf import settings

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotCommand, BotDescription, BotMessage, BotVariant, ButtonTypesEnum, BotLogs, \
    MessageTypeEnum
from bot_constructor.log_configs import logger_django
from bots.models import Bot, Message, Variant, Command


class BotApiByDjangoORM(IBotApi):
    def set_suite(self, suite_url: str):
        raise NotImplementedError('Метод не определен!')

    def sign_up(self, username: str, email: str, password: str):
        raise NotImplementedError('Метод не определен!')

    def authentication(self, username: str, password: str) -> None:
        raise NotImplementedError('Метод не определен!')

    def auth_by_token(self, token: str) -> None:
        raise NotImplementedError('Метод не определен!')

    def logout(self) -> None:
        raise NotImplementedError('Метод не определен!')

    def create_bot(self, bot_name: str,
                   bot_token: str, bot_description: str) -> BotDescription:
        raise NotImplementedError('Метод не определен!')

    def get_bots(self) -> List[BotDescription]:
        raise NotImplementedError('Метод не определен!')

    def get_bot_by_id(self, bot_id: int) -> BotDescription:
        """
        Получить объект бота с заданным идентификатором
        Args:
            bot_id: идентификатор бота

        Returns:
            объект бота
        """
        bot = Bot.objects.get(id=bot_id)
        if not bot:
            raise BotApiException(f'Ошибка при получении бота № {bot_id}')
        return self._create_bot_obj_from_data(bot)

    def change_bot(self, bot: BotDescription) -> None:
        raise NotImplementedError('Метод не определен!')

    def delete_bot(self, bot_id: int) -> None:
        raise NotImplementedError('Метод не определен!')

    def set_bot_start_message(self, bot: BotDescription,
                              start_message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def set_bot_error_message(self, bot: BotDescription,
                              error_message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def get_messages(self, bot: BotDescription) -> List[BotMessage]:
        """
        Получить все сообщения заданного бота
        Args:
            bot: бот, у которого нужно получить сообщения

        Returns:
            список сообщений бота
        """
        messages = Message.objects.filter(bot__id=bot.id)
        messages_list: List[BotMessage] = []
        for message in messages:
            messages_list.append(self._create_bot_message_from_data(message))
        return messages_list

    def create_message(self, bot: BotDescription, text: str,
                       keyboard_type: ButtonTypesEnum, x: int, y: int) -> BotMessage:
        raise NotImplementedError('Метод не определен!')

    def get_image_data_by_url(self, url: Optional[str]) -> Optional[bytes]:
        raise NotImplementedError('Метод не определен!')

    def get_one_message(self, message_id: int) -> BotMessage:
        raise NotImplementedError('Метод не определен!')

    def change_message(self, message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def remove_message_image(self, message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def remove_message_video(self, message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def delete_message(self, message: BotMessage):
        raise NotImplementedError('Метод не определен!')

    def get_variants(self, message: BotMessage) -> List[BotVariant]:
        """
        Получить варианты для заданного сообщения
        Args:
            message: сообщение для которого получаем варианты

        Returns:
            список вариантов
        """
        variants = Variant.objects.filter(current_message__id=message.id)
        variants_list: List[BotVariant] = []
        for variant in variants:
            variants_list.append(self._create_variant_from_data(variant))
        return variants_list

    def create_variant(self, message: BotMessage, text: str) -> BotVariant:
        raise NotImplementedError('Метод не определен!')

    def change_variant(self, variant: BotVariant) -> None:
        raise NotImplementedError('Метод не определен!')

    def connect_variant(self, variant: BotVariant,
                        message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def delete_variant(self, variant: BotVariant) -> None:
        raise NotImplementedError('Метод не определен!')

    def get_commands(self, bot: BotDescription) -> List[BotCommand]:
        """
        Получить команды для заданного бота

        Args:
            bot: бот для которого получаем команды

        Returns:
            список команд
        """
        commands = Command.objects.filter(bot__id=bot.id)
        commands_list = []
        for command in commands:
            commands_list.append(self._create_command_from_data(command))
        return commands_list

    def create_command(self, bot: BotDescription, command: str, description: str) -> BotCommand:
        raise NotImplementedError('Метод не определен!')

    def generate_bot(self, bot: BotDescription) -> None:
        raise NotImplementedError('generate bot is not implemented')

    def start_bot(self, bot: BotDescription) -> None:
        raise NotImplementedError('is not implemented')

    def stop_bot(self, bot: BotDescription) -> None:
        raise NotImplementedError('is not implemented')

    def get_running_bots_info(self) -> List[int]:
        raise NotImplementedError('is not implemented')

    def get_bot_logs(self, bot: BotDescription) -> BotLogs:
        raise NotImplementedError('is not implemented')

    def _create_bot_obj_from_data(self, bot_django: Bot) -> BotDescription:
        """Создает объект класса BotDescription из входящих данных"""
        bot_description = BotDescription()
        bot_description.id = bot_django.id
        bot_description.bot_name = bot_django.name
        bot_description.bot_token = bot_django.token
        bot_description.bot_description = bot_django.description
        bot_description.start_message_id = bot_django.start_message.id if bot_django.start_message is not None else None
        bot_description.error_message_id = bot_django.error_message.id if bot_django.error_message is not None else None
        return bot_description

    def _create_bot_message_from_data(self, message_django: Message) -> BotMessage:
        """Создает объект класса BotMessage из входящих данных"""
        bot_message = BotMessage()
        bot_message.id = message_django.id
        bot_message.text = message_django.text
        bot_message.keyboard_type = ButtonTypesEnum(message_django.keyboard_type)
        if message_django.photo:
            bot_message.photo = message_django.photo.path
        if message_django.video:
            bot_message.video = message_django.video.path
        if message_django.file:
            bot_message.file = message_django.file.path
        bot_message.x = message_django.coordinate_x
        bot_message.y = message_django.coordinate_y
        bot_message.message_type = MessageTypeEnum(message_django.message_type)

        bot_message.next_message_id = (
            message_django.next_message.id
            if message_django.next_message is not None
            else None
        )

        bot_message.variable = message_django.variable
        return bot_message

    def _create_variant_from_data(self, variant_django: Variant) -> BotVariant:
        """Создает объект класса BotMessage из входящих данных"""
        variant = BotVariant()
        variant.id = variant_django.id
        variant.text = variant_django.text
        variant.current_message_id = variant_django.current_message.id
        variant.next_message_id = (
            variant_django.next_message.id
            if variant_django.next_message is not None
            else None
        )
        return variant

    def _create_command_from_data(self, command_django: Command) -> BotCommand:
        """Создает объект класса BotCommand из входящих данных"""
        command = BotCommand()
        command.id = command_django.id
        command.bot_id = command_django.bot.id
        command.command = command_django.command
        command.description = command_django.description
        return command

    def _get_full_path_to_django_image(self, path_from_django: Optional[ImageFieldFile]) -> Optional[str]:
        """Получение полного пути к медиа файлу

        Args:
            path_from_django (Optional[ImageFieldFile]): Данные о изображении из БД, в Django формате

        Returns:
            Optional[str]: Полный путь к медиа файлу
        """
        assert isinstance(path_from_django, Optional[ImageFieldFile])
        if not path_from_django:
            result = None
        else:
            result = path_from_django.path
        return result

    def _get_file_format(self, django_file_field: Optional[FieldFile]) -> Optional[str]:
        """
        Получить формат файла.

        Args:
            django_file_field (Optional[FieldFile]): путь к файлу

        Returns:
            Optional[str]: формат файла
        """
        assert isinstance(django_file_field, Optional[FieldFile])
        if django_file_field:
            extension = Path(django_file_field.path).suffix
            result = extension.strip('.')
        else:
            result = None
        return result
