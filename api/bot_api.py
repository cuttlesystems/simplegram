import json
import typing
from typing import List, Optional

import requests

from api.data_objects import BotDescription, BotMessage, MessageVariant


class BotApi:
    def __init__(self, suite_url: str):
        """
        Создать объект для работы с данными ботов через rest_api
        :param suite_url: адрес сайта, откуда вызываем методы API
        """
        self._suite_url: str = suite_url
        self._auth_token: Optional[str] = None

    def authentication(self, username: str, password: str) -> None:
        """
        Провести аутентификацию пользователя и запомнить токен авторизации для
        дальнейшего вызова методов
        :param username: имя пользователя
        :param password: пароль
        """
        response = requests.post(
            self._suite_url + 'api/auth/token/login/',
            {
                'username': username,
                'password': password
            }
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception('Ошибка аутентификации пользователя {0}'.format(response.text))
        self._auth_token = json.loads(response.text)['auth_token']

    def create_bot(self, bot_name: str, bot_token: str, bot_description: str) -> BotDescription:
        """
        Создать бота
        :param bot_name: название бота
        :param bot_token: токен бота
        :param bot_description: описание бота
        :return: идентификатор созданного бота
        """
        response = requests.post(
            self._suite_url + 'api/bots/',
            {
                'name': bot_name,
                'token': bot_token,
                'description': bot_description
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.created:
            raise Exception('Ошибка при создании бота: {0}'.format(response.text))
        return self._create_bot_obj_from_dict(json.loads(response.text))

    def get_bots(self) -> List[BotDescription]:
        """
        Получить список ботов пользователя
        :return: список ботов
        """
        response = requests.get(
            self._suite_url + 'api/bots/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception('Ошибка при получении списка ботов')
        bots_dict_list: List[dict] = json.loads(response.text)
        bots_list: List[BotDescription] = []
        for bot_dict in bots_dict_list:
            bots_list.append(self._create_bot_obj_from_dict(bot_dict))
        return bots_list

    def get_bot_by_id(self, id: int) -> BotDescription:
        """
        Получить объект бота с заданным идентификатором
        :param id: идентификатор бота
        :return: объект бота
        """
        response = requests.get(
            self._suite_url + f'api/bots/{id}/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception('Ошибка при получении списка ботов')

        return self._create_bot_obj_from_dict(json.loads(response.text))

    def create_message(self, bot: BotDescription, text: str, x: int, y: int) -> BotMessage:
        """
        Создать сообщение
        :param bot: объект бота, для которого создается сообщение
        :param text: тест сообщения
        :param x: координата по x
        :param y: координата по y
        :return: идентификатор созданного сообщения
        """
        assert isinstance(bot, BotDescription)
        response = requests.post(
            self._suite_url + f'api/bots/{bot.id}/messages/',
            {
                'text': text,
                'coordinate_x': x,
                'coordinate_y': y,
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.created:
            raise Exception('Ошибка при создании сообщения: {0}'.format(response.text))
        return self._create_bot_message_from_dict(json.loads(response.text))

    def get_messages(self, bot: BotDescription) -> List[BotMessage]:
        """
        Получить все сообщения заданного бота
        :param bot: бот, у которого нужно получить сообщения
        :return: список сообщений бота
        """
        assert isinstance(bot, BotDescription)
        response = requests.get(
            self._suite_url + f'api/bots/{bot.id}/messages/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception(f'Ошибка при получении сообщений бота {response.text}')
        messages_list: List[BotMessage] = []
        for message_dict in json.loads(response.text):
            messages_list.append(self._create_bot_message_from_dict(message_dict))
        return messages_list

    def create_variant(self, message: BotMessage, text: str) -> MessageVariant:
        """
        Создание варианта
        :param message: объект сообщения для которого создается вариант
        :param text: текст создаваемого варианта
        :return: идентификатор созданного варианта
        """
        assert isinstance(message, BotMessage)
        response = requests.post(
            self._suite_url + f'api/messages/{message.id}/variants/',
            {
                'text': text
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.created:
            raise Exception('Ошибка при создании варианта: {0}'.format(response.text))
        return self._create_variant_from_dict(json.loads(response.text))

    def get_variants(self, message: BotMessage) -> List[MessageVariant]:
        """
        Получить варианты для заданного сообщения
        :param message: сообщение для которого получаем варианты
        :return: список вариантов
        """
        assert isinstance(message, BotMessage)
        response = requests.get(
            self._suite_url + f'api/messages/{message.id}/variants/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception(
                f'Ошибка при получении списка вариантов для сообщения {response.text}')
        variants: List[MessageVariant] = []
        variants_dict_list: List[dict] = json.loads(response.text)
        for variant_dict in variants_dict_list:
            variants.append(self._create_variant_from_dict(variant_dict))
        return variants

    def connect_variant(self, variant: MessageVariant, message: BotMessage) -> None:
        """
        Связать вариант и сообщение к которому перейдем при выборе этого варианта
        :param variant: связываемый вариант
        :param message: сообщение к которому перейдем
        """
        assert isinstance(variant, MessageVariant)
        assert isinstance(message, BotMessage)
        response = requests.patch(
            self._suite_url + f'api/variant/{variant.id}/',
            {
                'next_message': message.id
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception(
                'Ошибка при связывании варианта с последующим сообщением: {0}'.format(response.text))

    def set_bot_start_message(self, bot: BotDescription, start_message: BotMessage) -> None:
        """
        Установить сообщение с которого начнется работа с ботом
        :param bot: объект бота
        :param start_message: объект сообщения, которое будет установлено в качестве стартового
        в качестве стартового
        """
        assert isinstance(bot, BotDescription)
        assert isinstance(start_message, BotMessage)
        response = requests.patch(
            self._suite_url + 'api/bots/{0}/'.format(bot.id),
            {
                'start_message': start_message.id
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception('Ошибка при установке стартового сообщения бота: {0}'.format(
                response.text))

    def _get_headers(self) -> typing.Dict[str, str]:
        assert self._auth_token is not None
        return {
            'Authorization': 'Token ' + self._auth_token
        }

    def _create_bot_obj_from_dict(self, bot_dict: dict) -> BotDescription:
        bot_description = BotDescription()
        bot_description.id = bot_dict['id']
        bot_description.bot_name = bot_dict['name']
        bot_description.bot_token = bot_dict['token']
        bot_description.bot_description = bot_dict['description']
        bot_description.start_message_id = bot_dict['start_message']
        return bot_description

    def _create_bot_message_from_dict(self, message_dict: dict) -> BotMessage:
        bot_message = BotMessage()
        bot_message.id = message_dict['id']
        bot_message.text = message_dict['text']
        bot_message.photo = message_dict['photo']
        bot_message.video = message_dict['video']
        bot_message.file = message_dict['file']
        bot_message.x = message_dict['coordinate_x']
        bot_message.y = message_dict['coordinate_y']
        return bot_message

    def _create_variant_from_dict(self, variant_dict: dict) -> MessageVariant:
        variant = MessageVariant()
        variant.id = variant_dict['id']
        variant.text = variant_dict['text']
        variant.next_message_id = variant_dict['next_message']
        return variant
