from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file
from b_logic.data_objects import BotCommand


def generate_commands_code(commands: list[BotCommand]) -> str:
    """
    Генерирует код функции для добавления команд бота.

    Args:
        commands (list[BotCommand]): Список объектов BotCommand

    Returns:
        str: Сгенерированный код
    """
    list_of_commands = []
    for command in commands:
        list_of_commands.append(
            f'types.BotCommand("{command.command}", "{command.description}")'
        )
    content = f'await dp.bot.set_my_commands([{", ".join(list_of_commands)}])'
    config_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'on_startup_set_commands.txt')
    code = read_file(config_sample)
    code = code.format(commands_content=content)
    return code
