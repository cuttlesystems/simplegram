from cuttle_builder.bot_generator import BotGenerator
from cuttle_builder.bot_test_data import BotTestData


if __name__ == '__main__':
    test_data = BotTestData()
    botGenerator = BotGenerator(
        test_data.messages,
        test_data.variants,
        test_data.start_message_id,
        95)
    botGenerator.create_bot()
