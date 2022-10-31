import json
import uuid

import requests

SUITE_ADDR = 'http://127.0.0.1:8000/'
USER_ID = 2


def gen_unique_str() -> str:
    return str(uuid.uuid4()).replace('-', '')[:8]


def create_bot(user_id: int) -> int:
    """
    Создать бота
    :param user_id: идентификатор пользователя, для которого создаем бота
    :return: идентификатор созданного бота
    """
    response = requests.post(
        SUITE_ADDR + 'api/bots/',
        {
            'name': 'Имя тестовое бота {0}'.format(gen_unique_str()),
            'token': gen_unique_str(),
            'description': 'Описание созданного бота',
            'owner': user_id
        }
    )
    if response.status_code != requests.status_codes.codes.created:
        raise Exception('Ошибка при создании бота: {0}'.format(response.text))
    return json.loads(response.text)['id']


def create_message(bot_id: int, text: str, x: int, y: int) -> int:
    """
    Создать сообщение
    :param bot_id: идентификатор бота, для которого создается сообщение
    :param text: тест сообщения
    :param x: координата по x
    :param y: координата по y
    :return: идентификатор созданного сообщения
    """
    response = requests.post(
        SUITE_ADDR + 'api/messages/',
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


if __name__ == '__main__':
    bot_id = create_bot(USER_ID)
    
