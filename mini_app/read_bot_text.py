from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from app_tests.connection_settings import ConnectionSettings


if __name__ == '__main__':
    settings = ConnectionSettings()
    bot_api = BotApiByRequests(settings.site_addr)
    bot_api.authentication(settings.username, settings.password)
    bot = bot_api.get_bot_by_id(settings.bot_id)
    print(bot)
    commands = bot_api.get_commands(bot)
    for command in commands:
        print(f'    {command}')
    messages = bot_api.get_messages(bot)
    for message in messages:
        print(f'    Message: id={message.id}, '
              f'text={message.text}, '
              f'next_message_id={message.next_message_id}, '
              f'variable={message.variable is None} '
              f'messagetype={message.message_type} '
              f'photo={message.photo} '
              f'variable={message.variable}')
        variants = bot_api.get_variants(message)
        for variant in variants:
            print('    ' * 2, variant)
