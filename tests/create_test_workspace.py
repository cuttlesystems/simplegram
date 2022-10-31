import json
import uuid

import requests

SUITE_ADDR = 'http://127.0.0.1:8000/'
USER_ID = 3


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


def create_variant(message_id: int, text: str) -> int:
    """
    Создание варианта
    :param message_id: идентификатор сообщения для которого создается вариант
    :param text: текст создаваемого варианта
    :return: идентификатор созданного варианта
    """
    response = requests.post(
        SUITE_ADDR + 'api/variants/',
        {
            'text': text,
            'current_message': message_id
        }
    )
    if response.status_code != requests.status_codes.codes.created:
        raise Exception('Ошибка при создании варианта: {0}'.format(response.text))
    return json.loads(response.text)['id']


def set_bot_start_message(bot_id: int, start_message_id: int):
    response = requests.patch(
        SUITE_ADDR + 'api/bots/{0}/'.format(bot_id),
        {
            'start_message': start_message_id
        }
    )
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    bot_id = create_bot(USER_ID)
    other_message_id = create_message(bot_id, 'Другое сообщение', 100, 130)
    main_message_id = create_message(bot_id, 'Стартовое сообщение', 10, 10)
    create_variant(main_message_id, 'Вариант 1')
    create_variant(main_message_id, 'Вариант 2')
    create_variant(main_message_id, 'Вариант 3')
    set_bot_start_message(bot_id, main_message_id)

