from cuttle_builder.bot_generator import BotGenerator
from cuttle_builder.bot_test_data import BotTestData


if __name__ == '__main__':
    test_data = BotTestData()
    bot_generator = BotGenerator(
        test_data.messages,
        test_data.variants,
        test_data.commands,
        test_data.start_message_id,
        test_data.token,
        test_data.bot_directory,
        test_data.error_message_id
    )
    bot_generator.create_bot()
