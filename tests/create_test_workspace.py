import uuid
from api.bot_api import BotApi


def gen_unique_str() -> str:
    return str(uuid.uuid4()).replace('-', '')[:8]


SUITE_ADDR = 'http://127.0.0.1:8000/'
USERNAME = 'test_user'
PASSWORD = '123'


if __name__ == '__main__':
    bot_api = BotApi(SUITE_ADDR)
    bot_api.authentication('test_user', '123')

    bot = bot_api.create_bot(
        'Имя тестовое бота {0}'.format(gen_unique_str()),
        gen_unique_str(),
        'Описание созданного бота')

    main_message = bot_api.create_message(bot.id, 'Что вас интересует?', 10, 10)
    bot_api.set_bot_start_message(bot.id, main_message.id)
    mobile_variant_id = bot_api.create_variant(main_message.id, 'Телефоны')
    computer_variant_id = bot_api.create_variant(main_message.id, 'Компьютеры')
    appliances_variant_id = bot_api.create_variant(main_message.id, 'Бытовая техника')

    mobile_message = bot_api.create_message(bot.id, 'Какие телефоны предпочитаете?', 100, 130)
    bot_api.connect_variant(mobile_variant_id, mobile_message.id)

    computer_message = bot_api.create_message(bot.id, 'Какие компьютеры предпочитаете?', 200, 150)
    bot_api.connect_variant(computer_variant_id, computer_message.id)

    android_variant_id = bot_api.create_variant(mobile_message.id, 'Android')
    iphone_variant_id = bot_api.create_variant(mobile_message.id, 'IPhone')
    mobile_cancel_variant_id = bot_api.create_variant(mobile_message.id, 'Вернуться в начало')

    android_select_message = bot_api.create_message(
        bot.id, 'Выберите телефон который хотите приобрести', 200, 250)
    bot_api.connect_variant(android_variant_id, android_select_message.id)
    samsung_galaxy_s22 = bot_api.create_variant(android_select_message.id, 'Samsung Galaxy S22')
    samsung_galaxy_a53 = bot_api.create_variant(android_select_message.id, 'Samsung Galaxy A53')

    buy_samsung_galaxy_s22_message = bot_api.create_message(
        bot.id, 'Вы оформляете заказ Samsung Galaxy S22', 300, 150)
    bot_api.connect_variant(samsung_galaxy_s22, buy_samsung_galaxy_s22_message.id)

    buy_samsung_galaxy_a53_message = bot_api.create_message(
        bot.id, 'Вы оформляете заказ Samsung Galaxy A53', 300, 200)
    bot_api.connect_variant(samsung_galaxy_a53, buy_samsung_galaxy_a53_message.id)

    iphone_select_message = bot_api.create_message(
        bot.id, 'Выберите модель IPhone, которую хотите приобрести', 200, 300)
    bot_api.connect_variant(iphone_variant_id, iphone_select_message.id)

    iphone_13_variant = bot_api.create_variant(iphone_select_message.id, 'IPhone 13')
    iphone_14_variant = bot_api.create_variant(iphone_select_message.id, 'IPhone 14')

    buy_iphone_13_message = bot_api.create_message(bot.id, 'Вы оформляете заказ IPhone 13', 300, 300)
    bot_api.connect_variant(iphone_13_variant, buy_iphone_13_message.id)

    buy_iphone_14_message = bot_api.create_message(bot.id, 'Вы оформляете заказ IPhone 14', 300, 350)
    bot_api.connect_variant(iphone_14_variant, buy_iphone_14_message.id)

    bot_api.connect_variant(mobile_cancel_variant_id, main_message.id)
