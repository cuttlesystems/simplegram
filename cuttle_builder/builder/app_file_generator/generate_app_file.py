from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file
from b_logic.data_objects import BotDescription


def generate_app_file_code(imports: str, logs_directory: str) -> str:
    """
    Генерирует код app файла (исполняемый файл бота).

    Args:
        imports (str): Импорты.
        logs_directory (str): Директория для хранения логов бота.

    Returns:
        str: Сгенерированный код
    """
    app_file_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'app_sample.txt')
    code = read_file(app_file_sample)
    code = code.format(imports=imports, logs_directory=repr(logs_directory))
    return code
