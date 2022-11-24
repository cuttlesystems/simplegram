import json
import typing
from typing import List, Optional
import requests

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException
from b_logic.data_objects import BotDescription, BotMessage, MessageVariant


class BotApiByRequests(IBotApi):
    def __init__(self, suite_url: typing.Optional[str] = None):
        """
        Создать объект для работы с данными ботов через rest_api
        Args:
            suite_url: адрес сайта, откуда вызываем методы API
        """
        self._suite_url: str = suite_url
        self._auth_token: Optional[str] = None

    def set_suite(self, suite_url: str):
        """Устанавливает suite_url: корневой URL для API запросов"""
        assert isinstance(suite_url, str)
        self._suite_url = suite_url

    def authentication(self, username: str, password: str) -> None:
        """
        Провести аутентификацию пользователя и запомнить токен авторизации для
        дальнейшего вызова методов
        Args:
            username: имя пользователя
            password: пароль
        """
        try:
            response = requests.post(
                self._suite_url + 'api/auth/token/login/',
                {
                    'username': username,
                    'password': password
                }
            )
            if response.status_code != requests.status_codes.codes.ok:
                raise BotApiException('Ошибка аутентификации пользователя {0}'.format(response.text))
            self._auth_token = json.loads(response.text)['auth_token']
        except requests.exceptions.ConnectionError as connection_error:
            raise BotApiException('Ошибка подключения')

    def auth_by_token(self, token: str) -> None:
        """
        Авторизация пользователя по токену
        Args:
            token: токен авторизации
        """
        assert isinstance(token, str)
        self._auth_token = token

    def create_bot(self, bot_name: str, bot_token: str, bot_description: str) -> BotDescription:
        """
        Создать бота
        Args:
            bot_name: название бота
            bot_token: токен бота
            bot_description: описание бота

        Returns:
            объект созданного бота
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
            raise BotApiException('Ошибка при создании бота: {0}'.format(response.text))
        return self._create_bot_obj_from_data(json.loads(response.text))

    def get_bots(self) -> List[BotDescription]:
        """
        Получить список ботов пользователя
        Returns:
            список ботов
        """
        response = requests.get(
            self._suite_url + 'api/bots/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException('Ошибка при получении списка ботов')
        bots_dict_list: List[dict] = json.loads(response.text)
        bots_list: List[BotDescription] = []
        for bot_dict in bots_dict_list:
            bots_list.append(self._create_bot_obj_from_data(bot_dict))
        return bots_list

    def get_bot_by_id(self, id: int) -> BotDescription:
        """
        Получить объект бота с заданным идентификатором
        Args:
            id: идентификатор бота

        Returns:
            объект бота
        """
        response = requests.get(
            self._suite_url + f'api/bots/{id}/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException(f'Ошибка при получении списка ботов {response.text}')

        return self._create_bot_obj_from_data(json.loads(response.text))

    def change_bot(self, bot: BotDescription) -> None:
        assert isinstance(bot.id, int)
        response = requests.patch(
            self._suite_url + f'api/bots/{bot.id}/',
            {
                'name': bot.bot_name,
                'token': bot.bot_token,
                'description': bot.bot_description
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException('Ошибка при изменении бота')

    def delete_bot(self, id: int) -> None:
        """
        Удалить бота
        Args:
            id: идентификатор бота
        """
        response = requests.delete(
            self._suite_url + f'api/bots/{id}/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.no_content:
            raise BotApiException(f'Ошибка при удалении бота')

    def create_message(self, bot: BotDescription, text: str, x: int, y: int) -> BotMessage:
        """
        Создать сообщение
        Args:
            bot: объект бота, для которого создается сообщение
            text: тест сообщения
            x: координата по x
            y: координата по y

        Returns:
            объект созданного сообщения
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
            raise BotApiException('Ошибка при создании сообщения: {0}'.format(response.text))
        return self._create_bot_message_from_data(json.loads(response.text))

    def get_messages(self, bot: BotDescription) -> List[BotMessage]:
        """
        Получить все сообщения заданного бота
        Args:
            bot: бот, у которого нужно получить сообщения

        Returns:
            список сообщений бота
        """
        assert isinstance(bot, BotDescription)
        response = requests.get(
            self._suite_url + f'api/bots/{bot.id}/messages/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException(f'Ошибка при получении сообщений бота {response.text}')
        messages_list: List[BotMessage] = []
        for message_dict in json.loads(response.text):
            messages_list.append(self._create_bot_message_from_data(message_dict))
        return messages_list

    def create_variant(self, message: BotMessage, text: str) -> MessageVariant:
        """
        Создание варианта
        Args:
            message: объект сообщения для которого создается вариант
            text: текст создаваемого варианта

        Returns:
            объект созданного варианта
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
            raise BotApiException('Ошибка при создании варианта: {0}'.format(response.text))
        return self._create_variant_from_data(json.loads(response.text))

    def get_variants(self, message: BotMessage) -> List[MessageVariant]:
        """
        Получить варианты для заданного сообщения
        Args:
            message: сообщение для которого получаем варианты

        Returns:
            список вариантов
        """
        assert isinstance(message, BotMessage)
        response = requests.get(
            self._suite_url + f'api/messages/{message.id}/variants/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException(
                f'Ошибка при получении списка вариантов для сообщения {response.text}')
        variants: List[MessageVariant] = []
        variants_dict_list: List[dict] = json.loads(response.text)
        for variant_dict in variants_dict_list:
            variants.append(self._create_variant_from_data(variant_dict))
        return variants

    def connect_variant(self, variant: MessageVariant, message: BotMessage) -> None:
        """
        Связать вариант и сообщение, к которому перейдем при выборе этого варианта
        Args:
            variant: связываемый вариант
            message: сообщение к которому перейдем
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
            raise BotApiException(
                'Ошибка при связывании варианта с последующим сообщением: {0}'.format(response.text))

    def set_bot_start_message(self, bot: BotDescription, start_message: BotMessage) -> None:
        """
        Установить сообщение с которого начнется работа с ботом
        Args:
            bot: объект бота
            start_message: объект сообщения, которое будет установлено в качестве стартового
        в качестве стартового
        """
        assert isinstance(bot, BotDescription)
        assert isinstance(start_message, BotMessage)
        response = requests.patch(
            self._suite_url + f'api/bots/{bot.id}/',
            {
                'start_message': start_message.id
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException('Ошибка при установке стартового сообщения бота: {0}'.format(
                response.text))

    def delete_message(self, message: BotMessage):
        assert isinstance(message, BotMessage)
        print(f'delete message id {message.id}')
        response = requests.delete(
            self._suite_url + f'api/message/{message.id}/',
            headers=self._get_headers()
        )
        print(f'delete response {response.status_code}')
        if response.status_code != requests.status_codes.codes.no_content:
            raise BotApiException(f'Ошибка при удалении сообщения: {response.text}')

    def change_message(self, message: BotMessage) -> None:
        assert isinstance(message, BotMessage)
        response = requests.patch(
            self._suite_url + f'api/message/{message.id}/',
            {
                # todo: тут надо доделать, чтобы менялись все поля. И сделать цивилизованно
                'coordinate_x': message.x,
                'coordinate_y': message.y
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotApiException(
                'Ошибка при изменении сообщения: {0}'.format(response.text))

    def _get_headers(self) -> typing.Dict[str, str]:
        """
        Получить словарь заголовков, которые добавляются к запросам.
        Содержит информацию об авторизации.
        Returns:
            словарь с заголовками для запроса
        """
        assert self._auth_token is not None
        return {
            'Authorization': 'Token ' + self._auth_token
        }

    def _create_bot_obj_from_data(self, bot_dict: dict) -> BotDescription:
        """Создает объект класса BotDescription из входящих данных"""
        bot_description = BotDescription()
        bot_description.id = bot_dict['id']
        bot_description.bot_name = bot_dict['name']
        bot_description.bot_token = bot_dict['token']
        bot_description.bot_description = bot_dict['description']
        bot_description.start_message_id = bot_dict['start_message']
        return bot_description

    def _create_bot_message_from_data(self, message_dict: dict) -> BotMessage:
        """Создает объект класса BotMessage из входящих данных"""
        bot_message = BotMessage()
        bot_message.id = message_dict['id']
        bot_message.text = message_dict['text']
        bot_message.photo = message_dict['photo']
        bot_message.video = message_dict['video']
        bot_message.file = message_dict['file']
        bot_message.x = message_dict['coordinate_x']
        bot_message.y = message_dict['coordinate_y']
        return bot_message

    def _create_variant_from_data(self, variant_dict: dict) -> MessageVariant:
        """Создает объект класса MessageVariant из входящих данных"""
        variant = MessageVariant()
        variant.id = variant_dict['id']
        variant.text = variant_dict['text']
        variant.current_message_id = variant_dict['current_message']
        variant.next_message_id = variant_dict['next_message']
        return variant
