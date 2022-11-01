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


def connect_variant(variant_id: int, message_id: int) -> None:
    response = requests.patch(
        SUITE_ADDR + 'api/variants/{0}/'.format(variant_id),
        {
            'next_message': message_id
        }
    )
    if response.status_code != requests.status_codes.codes.ok:
        raise Exception(
            'Ошибка при связывании варианта с последующим сообщением: {0}'.format(response.text))


def set_bot_start_message(bot_id: int, start_message_id: int) -> None:
    """
    Установить сообщение с которого начнется работа с ботом
    :param bot_id: идентификатор бота
    :param start_message_id: идентификатор сообщения, которое будет установлено
    в качестве стартового
    """
    response = requests.patch(
        SUITE_ADDR + 'api/bots/{0}/'.format(bot_id),
        {
            'start_message': start_message_id
        }
    )
    if response.status_code != requests.status_codes.codes.ok:
        raise Exception('Ошибка при установке стартового сообщения бота: {0}'.format(
            response.text))


if __name__ == '__main__':
    bot_id = create_bot(USER_ID)

    main_message_id = create_message(bot_id, 'Что вас интересует?', 10, 10)
    set_bot_start_message(bot_id, main_message_id)
    mobile_variant_id = create_variant(main_message_id, 'Телефоны')
    computer_variant_id = create_variant(main_message_id, 'Компьютеры')
    appliances_variant_id = create_variant(main_message_id, 'Бытовая техника')

    mobile_message_id = create_message(bot_id, 'Какие телефоны предпочитаете?', 100, 130)
    connect_variant(mobile_variant_id, mobile_message_id)

    computer_message_id = create_message(bot_id, 'Какие компьютеры предпочитаете?', 200, 150)
    connect_variant(computer_variant_id, computer_message_id)

    android_variant_id = create_variant(mobile_message_id, 'Android')
    iphone_variant_id = create_variant(mobile_message_id, 'IPhone')
    mobile_cancel_variant_id = create_variant(mobile_message_id, 'Вернуться в начало')

    android_select_message_id = create_message(
        bot_id, 'Выберите телефон который хотите приобрести', 200, 250)
    connect_variant(android_variant_id, android_select_message_id)
    samsung_galaxy_s22 = create_variant(android_select_message_id, 'Samsung Galaxy S22')
    samsung_galaxy_a53 = create_variant(android_select_message_id, 'Samsung Galaxy A53')
