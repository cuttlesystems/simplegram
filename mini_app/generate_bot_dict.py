from cuttle_builder.bot_generator import BotGenerator
from cuttle_builder.bot_test_data import BotTestData


if __name__ == '__main__':
    test_data = BotTestData()
    bot_generator = BotGenerator(
        messages=test_data.messages,
        variants=test_data.variants,
        commands=test_data.commands,
        bot=test_data.bot,
        bot_path=test_data.bot_directory,
    )
    bot_generator.create_bot()
