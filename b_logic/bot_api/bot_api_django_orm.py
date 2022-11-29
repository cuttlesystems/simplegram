from typing import List

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotDescription, BotMessage, BotVariant
from bots.models import Bot, Message, Variant


class BotApiByDjangoORM(IBotApi):
    def set_suite(self, suite_url: str):
        raise NotImplementedError('Метод не определен!')

    def authentication(self, username: str, password: str) -> None:
        raise NotImplementedError('Метод не определен!')

    def auth_by_token(self, token: str) -> None:
        raise NotImplementedError('Метод не определен!')

    def create_bot(self, bot_name: str,
                   bot_token: str, bot_description: str) -> BotDescription:
        raise NotImplementedError('Метод не определен!')

    def get_bots(self) -> List[BotDescription]:
        raise NotImplementedError('Метод не определен!')

    def get_bot_by_id(self, id: int) -> BotDescription:
        """
        Получить объект бота с заданным идентификатором
        Args:
            id: идентификатор бота

        Returns:
            объект бота
        """
        bot = Bot.objects.get(id=id)
        if not bot:
            raise BotApiException(f'Ошибка при получении бота № {id}')
        return self._create_bot_obj_from_data(bot)

    def change_bot(self, bot: BotDescription) -> None:
        raise NotImplementedError('Метод не определен!')

    def delete_bot(self, id: int) -> None:
        raise NotImplementedError('Метод не определен!')

    def create_message(self, bot: BotDescription,
                       text: str, x: int, y: int) -> BotMessage:
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

    def create_variant(self, message: BotMessage, text: str) -> BotVariant:
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

    def connect_variant(self, variant: BotVariant,
                        message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def set_bot_start_message(self, bot: BotDescription,
                              start_message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def delete_message(self, message: BotMessage):
        raise NotImplementedError('Метод не определен!')

    def change_message(self, message: BotMessage) -> None:
        raise NotImplementedError('Метод не определен!')

    def _create_bot_obj_from_data(self, bot_django: Bot) -> BotDescription:
        """Создает объект класса BotDescription из входящих данных"""
        bot_description = BotDescription()
        bot_description.id = bot_django.id
        bot_description.bot_name = bot_django.name
        bot_description.bot_token = bot_django.token
        bot_description.bot_description = bot_django.description
        bot_description.start_message_id = bot_django.start_message.id
        return bot_description

    def _create_bot_message_from_data(self, message_django: Message) -> BotMessage:
        """Создает объект класса BotMessage из входящих данных"""
        bot_message = BotMessage()
        bot_message.id = message_django.id
        bot_message.text = message_django.text
        bot_message.keyboard_type = message_django.keyboard_type
        bot_message.photo = message_django.photo
        bot_message.video = message_django.video
        bot_message.file = message_django.file
        bot_message.x = message_django.coordinate_x
        bot_message.y = message_django.coordinate_y
        return bot_message

    def _create_variant_from_data(self, variant_django: Variant) -> BotVariant:
        """Создает объект класса BotMessage из входящих данных"""
        variant = BotVariant()
        variant.id = variant_django.id
        variant.text = variant_django.text
        variant.current_message_id = variant_django.current_message.id
        if variant_django.next_message:
            variant.next_message_id = variant_django.next_message.id
        else:
            variant.next_message_id = None
        return variant
