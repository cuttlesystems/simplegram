# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler
from typing import Optional


def prev_state_code_line(prev_state: Optional[str]) -> str:
    assert isinstance(prev_state, Optional[str])
    result = ''
    if prev_state == '*':
        result = 'state=\'*\''
    elif prev_state is not None:
        result = 'state=States.{0}'.format(prev_state)
    return result


def create_state_message_handler(imports: str, command: str, prev_state: Optional[str], text_to_handle: Optional[str],
                                 state_to_set_name: Optional[str], text_of_answer: str, image_answer: Optional[str],
                                 kb: Optional[str], additional_functions_from_top_of_answer: str, additional_functions_under_answer: str) -> str:
    """Подготовка данных для генерации кода меседж хэндлера

    Args:
        imports (str): Импорты
        command (str): Команда перехватываемая хэндлером типа /start
        prev_state (Optional[str]): Предыдущее состояние
        text_to_handle (Optional[str]): Текст перехватываемый хэндлером
        state_to_set_name (Optional[str]): Состояние к установке
        text_of_answer (str): Текст ответа
        image_answer (Optional[str]): Путь к файлу с изображением
        kb (str): Клавиатура
        additional_functions_from_top_of_answer

    Returns:
        str: Сгенерированный код
    """
    assert isinstance(imports, str)
    assert isinstance(command, str)
    assert isinstance(prev_state, Optional[str])
    assert isinstance(text_to_handle, Optional[str])
    assert isinstance(state_to_set_name, Optional[str])
    assert isinstance(text_of_answer, str)
    assert isinstance(image_answer, Optional[str])
    assert isinstance(kb, Optional[str])
    assert isinstance(additional_functions_from_top_of_answer, str)
    handler_sample_name = 'message_handler_sample.txt'
    list_of_handler_params = [
        command,
        'lambda message: message.text == {0}'.format(repr(text_to_handle)) if text_to_handle else '',
        prev_state_code_line(prev_state)
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    keyboard_if_exists = f', reply_markup={kb}' if kb else ""
    answer_content = f'await message.answer(text=f{repr(text_of_answer)}{keyboard_if_exists})'
    if image_answer:
        image_content = f'\n    await message.answer_photo(photo=types.InputFile(\'{image_answer}\'), caption=f{repr(text_of_answer)}{keyboard_if_exists})'
        answer_content = image_content

    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content,
                          handler_sample_name,
                          additional_functions_from_top_of_answer,
                          additional_functions_under_answer)


def create_state_callback_handler(imports: str, command: str, prev_state: Optional[str], text_to_handle: Optional[str],
                                  state_to_set_name: Optional[str], text_of_answer: str, image_answer: Optional[str],
                                  kb: Optional[str], additional_functions_from_top_of_answer: str, additional_functions_under_answer: str) -> str:
    """Подготовка данных для генерации кода колбэк хэндлера

    Args:
        imports (str): Импорты
        command (str): Команда перехватываемая хэндлером типа /start
        prev_state (Optional[str]): Предыдущее состояние
        text_to_handle (Optional[str]): Текст перехватываемый хэндлером
        state_to_set_name (Optional[str]): Состояние к установке
        send_message_type (str): Тип отправляемого сообщения
        text_of_answer (str): Текст ответа
        image_answer (Optional[str]): Путь к файлу с изображением
        kb (str): Клавиатура
        additional_functions_from_top_of_answer

    Returns:
        str: Сгенерированный код
    """
    assert isinstance(imports, str)
    assert isinstance(command, str)
    assert isinstance(prev_state, Optional[str])
    assert isinstance(text_to_handle, Optional[str])
    assert isinstance(state_to_set_name, Optional[str])
    assert isinstance(text_of_answer, str)
    assert isinstance(image_answer, Optional[str])
    assert isinstance(kb, Optional[str])
    assert isinstance(additional_functions_from_top_of_answer, str)
    handler_sample_name = 'callback_handler_sample.txt'
    list_of_handler_params = [
        command,
        'text = {0}'.format(repr(text_to_handle)) if text_to_handle else '',
        prev_state_code_line(prev_state)
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    keyboard_if_exists = f', reply_markup={kb}' if kb else ""
    answer_content = f'await callback.message.answer(text=f{repr(text_of_answer)}{keyboard_if_exists})'
    if image_answer:
        image_content = f'\n    await callback.message.answer_photo(photo=types.InputFile(\'{image_answer}\'))'
        answer_content += image_content

    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content,
                          handler_sample_name,
                          additional_functions_from_top_of_answer,
                          additional_functions_under_answer)
