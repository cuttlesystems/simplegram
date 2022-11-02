import uuid
from api.bot_api import BotApi


def gen_unique_str() -> str:
    return str(uuid.uuid4()).replace('-', '')[:8]


SUITE_ADDR = 'http://127.0.0.1:8000/'
USER_ID = 3

if __name__ == '__main__':
    bot_api = BotApi(SUITE_ADDR, USER_ID)
    bot_api.authentication('test_user', '123')
    bot_id = bot_api.create_bot(
        'Имя тестовое бота {0}'.format(gen_unique_str()),
        gen_unique_str(),
        'Описание созданного бота')

    main_message_id = bot_api.create_message(bot_id, 'Что вас интересует?', 10, 10)
    bot_api.set_bot_start_message(bot_id, main_message_id)
    mobile_variant_id = bot_api.create_variant(bot_id, main_message_id, 'Телефоны')
    computer_variant_id = bot_api.create_variant(bot_id, main_message_id, 'Компьютеры')
    appliances_variant_id = bot_api.create_variant(bot_id, main_message_id, 'Бытовая техника')

    mobile_message_id = bot_api.create_message(bot_id, 'Какие телефоны предпочитаете?', 100, 130)
    bot_api.connect_variant(bot_id, main_message_id, mobile_variant_id, mobile_message_id)

    computer_message_id = bot_api.create_message(bot_id, 'Какие компьютеры предпочитаете?', 200, 150)
    bot_api.connect_variant(bot_id, computer_variant_id, computer_message_id)

    android_variant_id = bot_api.create_variant(bot_id, mobile_message_id, 'Android')
    iphone_variant_id = bot_api.create_variant(bot_id, mobile_message_id, 'IPhone')
    mobile_cancel_variant_id = bot_api.create_variant(bot_id, mobile_message_id, 'Вернуться в начало')

    android_select_message_id = bot_api.create_message(
        bot_id, 'Выберите телефон который хотите приобрести', 200, 250)
    bot_api.connect_variant(bot_id, android_variant_id, android_select_message_id)
    samsung_galaxy_s22 = bot_api.create_variant(android_select_message_id, 'Samsung Galaxy S22')
    samsung_galaxy_a53 = bot_api.create_variant(android_select_message_id, 'Samsung Galaxy A53')

    buy_samsung_galaxy_s22_message = bot_api.create_message(
        bot_id, 'Вы оформляете заказ Samsung Galaxy S22', 300, 150)
    bot_api.connect_variant(bot_id, samsung_galaxy_s22, buy_samsung_galaxy_s22_message)

    buy_samsung_galaxy_a53_message = bot_api.create_message(
        bot_id, 'Вы оформляете заказ Samsung Galaxy A53', 300, 200)
    bot_api.connect_variant(bot_id, samsung_galaxy_a53, buy_samsung_galaxy_a53_message)

    iphone_select_message = bot_api.create_message(
        bot_id, 'Выберите модель IPhone, которую хотите приобрести', 200, 300)
    bot_api.connect_variant(bot_id, iphone_variant_id, iphone_select_message)

    iphone_13_variant = bot_api.create_variant(bot_id, iphone_select_message, 'IPhone 13')
    iphone_14_variant = bot_api.create_variant(bot_id, iphone_select_message, 'IPhone 14')

    buy_iphone_13_message = bot_api.create_message(bot_id, 'Вы оформляете заказ IPhone 13', 300, 300)
    bot_api.connect_variant(bot_id, iphone_13_variant, buy_iphone_13_message)

    buy_iphone_14_message = bot_api.create_message(bot_id, 'Вы оформляете заказ IPhone 14', 300, 350)
    bot_api.connect_variant(bot_id, iphone_14_variant, buy_iphone_14_message)

    bot_api.connect_variant(bot_id, mobile_cancel_variant_id, main_message_id)
