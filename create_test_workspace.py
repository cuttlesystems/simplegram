import uuid

from app_tests.connection_settings import ConnectionSettings
from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.data_objects import ButtonTypes


def gen_unique_str() -> str:
    return str(uuid.uuid4()).replace('-', '')[:8]


if __name__ == '__main__':
    settings = ConnectionSettings()
    bot_api = BotApiByRequests(settings.site_addr)
    bot_api.authentication(settings.username, settings.password)

    bot = bot_api.create_bot(
        'Имя тестовое бота {0}'.format(gen_unique_str()),
        '5689990303:AAEnr1DqNhBvx_zwVt9rnb2P3YJynvjq2rg',
        'Описание созданного бота')

    main_message = bot_api.create_message(bot, 'Что вас интересует?', ButtonTypes.REPLY, 10, 10)
    bot_api.set_bot_start_message(bot, main_message)
    mobile_variant = bot_api.create_variant(main_message, 'Телефоны')
    computer_variant = bot_api.create_variant(main_message, 'Компьютеры')
    appliances_variant = bot_api.create_variant(main_message, 'Бытовая техника')

    mobile_message = bot_api.create_message(bot, 'Какие телефоны предпочитаете?', ButtonTypes.REPLY, 100, 130)
    bot_api.connect_variant(mobile_variant, mobile_message)

    computer_message = bot_api.create_message(bot, 'Какие компьютеры предпочитаете?', ButtonTypes.REPLY, 200, 150)
    bot_api.connect_variant(computer_variant, computer_message)

    computer_message_variant_desc = bot_api.create_variant(computer_message, 'Прочитать описание компьютеров')
    computer_to_mobile_var = bot_api.create_variant(computer_message, 'Переключиться на айфоны')

    computer_description_message = bot_api.create_message(
        bot,
        'Тут будет длинное сообщение. Чтобы проверить, что будет если сообщение не '
        'помещается внутри прямоугольника для сообщения. Проверяем, что если сообщение еще длиннее. '
        'А если еще длиннее. И совсем длинное, которое не помещается',
        ButtonTypes.REPLY,
        500, 10)

    bot_api.connect_variant(computer_message_variant_desc, computer_description_message)


    android_variant = bot_api.create_variant(mobile_message, 'Android')
    iphone_variant = bot_api.create_variant(mobile_message, 'IPhone')
    mobile_cancel_variant = bot_api.create_variant(mobile_message, 'Вернуться в начало')

    android_select_message = bot_api.create_message(
        bot, 'Выберите телефон который хотите приобрести', ButtonTypes.REPLY, 200, 250)
    bot_api.connect_variant(android_variant, android_select_message)
    samsung_galaxy_s22 = bot_api.create_variant(android_select_message, 'Samsung Galaxy S22')
    samsung_galaxy_a53 = bot_api.create_variant(android_select_message, 'Samsung Galaxy A53')
    mobile_test_variant = bot_api.create_variant(android_select_message, 'Huawei')

    buy_samsung_galaxy_s22_message = bot_api.create_message(
        bot, 'Вы оформляете заказ Samsung Galaxy S22', ButtonTypes.REPLY, 300, 150)
    bot_api.connect_variant(samsung_galaxy_s22, buy_samsung_galaxy_s22_message)

    buy_samsung_galaxy_a53_message = bot_api.create_message(
        bot, 'Вы оформляете заказ Samsung Galaxy A53', ButtonTypes.REPLY, 300, 200)
    bot_api.connect_variant(samsung_galaxy_a53, buy_samsung_galaxy_a53_message)

    bot_mobile_test_mes = bot_api.create_message(
        bot, 'Оформляем Huawei', ButtonTypes.REPLY, 160, 180)
    bot_api.connect_variant(mobile_test_variant, bot_mobile_test_mes)

    iphone_select_message = bot_api.create_message(
        bot, 'Выберите модель IPhone, которую хотите приобрести', ButtonTypes.REPLY, 200, 300)
    bot_api.connect_variant(iphone_variant, iphone_select_message)

    iphone_13_variant = bot_api.create_variant(iphone_select_message, 'IPhone 13')
    iphone_14_variant = bot_api.create_variant(iphone_select_message, 'IPhone 14')

    bot_api.connect_variant(computer_to_mobile_var, iphone_select_message)

    buy_iphone_13_message = bot_api.create_message(bot, 'Вы оформляете заказ IPhone 13', ButtonTypes.REPLY, 300, 300)
    bot_api.connect_variant(iphone_13_variant, buy_iphone_13_message)

    buy_iphone_14_message = bot_api.create_message(bot, 'Вы оформляете заказ IPhone 14', ButtonTypes.REPLY, 300, 350)
    bot_api.connect_variant(iphone_14_variant, buy_iphone_14_message)

    bot_api.connect_variant(mobile_cancel_variant, main_message)

    print(f'Идентификатор созданного бота: {bot.id}')