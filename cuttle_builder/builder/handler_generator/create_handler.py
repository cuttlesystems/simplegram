# base method to create handler

from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file


def create_handler(imports: str, handler_text: str, name: str, state_content: str,
                   send_content: str, handler_sample_name: str, additional_functions: str) -> str:
    """Генерирует код хэндлера, подставляя значения в шаблон

    Args:
        imports (str): Импорты
        handler_text (str): Параметры хэндлера
        name (str): Часть имени функции
        state_content (str): Строка кода с переходом в нужное состояние
        send_content (str): Контент с ответом пользователю
        handler_sample_name (str): Шаблон для подстановки данных
        additional_functions (str): дополнительные функции хендлера

    Returns:
        str: Сгенерированный код
    """

    handler_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / handler_sample_name)
    # read sample and put settings from upper methods
    code = read_file(handler_sample)
    code = code.format(imports=imports,
                       handler_params=handler_text,
                       handler_name=name,
                       additional_functions=additional_functions,
                       state_to_set=state_content,
                       answer_content=send_content)
    code = code.replace('\t', '    ')
    return code
