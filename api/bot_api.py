import json
import requests


class BotApi:
    def __init__(self, suite_url: str, user_id: int):
        self._suite_url: str = suite_url
        self._user_id: int = user_id

    def create_bot(self, bot_name: str, bot_token: str, bot_description: str) -> int:
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
                'description': bot_description,
                'owner': self._user_id
            }
        )
        if response.status_code != requests.status_codes.codes.created:
            raise Exception('Ошибка при создании бота: {0}'.format(response.text))
        return json.loads(response.text)['id']

    def create_message(self, bot_id: int, text: str, x: int, y: int) -> int:
        """
        Создать сообщение
        :param bot_id: идентификатор бота, для которого создается сообщение
        :param text: тест сообщения
        :param x: координата по x
        :param y: координата по y
        :return: идентификатор созданного сообщения
        """
        response = requests.post(
            self._suite_url + 'api/messages/',
            {
                'bot': bot_id,
                'text': text,
                'coordinate_x': x,
                'coordinate_y': y,
            }
        )
        if response.status_code != requests.status_codes.codes.created:
            raise Exception('Ошибка при создании сообщения: {0}'.format(response.text))
        return json.loads(response.text)['id']

    def create_variant(self, message_id: int, text: str) -> int:
        """
        Создание варианта
        :param message_id: идентификатор сообщения для которого создается вариант
        :param text: текст создаваемого варианта
        :return: идентификатор созданного варианта
        """
        response = requests.post(
            self._suite_url + 'api/variants/',
            {
                'text': text,
                'current_message': message_id
            }
        )
        if response.status_code != requests.status_codes.codes.created:
            raise Exception('Ошибка при создании варианта: {0}'.format(response.text))
        return json.loads(response.text)['id']

    def connect_variant(self, variant_id: int, message_id: int) -> None:
        response = requests.patch(
            self._suite_url + 'api/variants/{0}/'.format(variant_id),
            {
                'next_message': message_id
            }
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception(
                'Ошибка при связывании варианта с последующим сообщением: {0}'.format(response.text))

    def set_bot_start_message(self, bot_id: int, start_message_id: int) -> None:
        """
        Установить сообщение с которого начнется работа с ботом
        :param bot_id: идентификатор бота
        :param start_message_id: идентификатор сообщения, которое будет установлено
        в качестве стартового
        """
        response = requests.patch(
            self._suite_url + 'api/bots/{0}/'.format(bot_id),
            {
                'start_message': start_message_id
            }
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise Exception('Ошибка при установке стартового сообщения бота: {0}'.format(
                response.text))
