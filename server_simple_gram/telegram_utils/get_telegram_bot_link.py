import json
from typing import Optional

import requests

TELEGRAM_API_URL = 'https://api.telegram.org'
LINK_TO_BOT = 'https://t.me/'


def get_bot_link(bot_token: Optional[str]) -> str:
    """
    Получает ссылку к телеграм боту по токену бота.

    Args:
        bot_token: токен бота

    Returns:
        Ссылка на телеграм бота в формате: (https://t.me/VasiaBot)
    """
    assert isinstance(bot_token, Optional[str])
    bot_username = ''
    if bot_token is None or bot_token == '':
        bot_username = 'Bot token is not specified.'
    else:
        try:
            response = requests.get(
                url=f'{TELEGRAM_API_URL}/bot{bot_token}/getMe',
            )
            if response.status_code == requests.status_codes.codes.ok:
                response_data = json.loads(response.text)
                bot_username = response_data['result']['username']
                bot_username = LINK_TO_BOT + bot_username
            elif response.status_code in [requests.status_codes.codes.not_found,
                                          requests.status_codes.codes.unauthorized]:
                bot_username = 'Information on provided token was not found.'
        except ConnectionError as error:
            bot_username = 'Check your internet connection.'
            print(f'-----> Logger: {error}')
    return bot_username
