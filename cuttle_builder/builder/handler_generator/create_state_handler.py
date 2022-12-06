# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler
from typing import Optional


def prev_state_code_line(prev_state: Optional[str]) -> str:
    result = ''
    if prev_state == '*':
        result = 'state=\'*\''
    elif prev_state is not None:
        result = 'state=States.{0}'.format(prev_state)
    return result


def create_state_message_handler(imports: str, command: str, prev_state: Optional[str], text_to_handle: Optional[str],
                                 state_to_set_name: Optional[str], send_message_type: str, text_of_answer: str, kb: str) -> str:
    """Подготовка данных для генерации кода меседж хэндлера

    Args:
        imports (str): Импорты
        command (str): Команда перехватываемая хэндлером типа /start
        prev_state (Optional[str]): Предыдущее состояние
        text_to_handle (Optional[str]): Текст перехватываемый хэндлером
        state_to_set_name (Optional[str]): Состояние к установке
        send_message_type (str): Тип отправляемого сообщения
        text_of_answer (str): Текст ответа
        kb (str): Клавиатура

    Returns:
        str: Сгенерированный код
    """

    handler_sample_name = 'message_handler_sample.txt'
    list_of_handler_params = [
        command,
        'lambda message: message.text == \'{0}\''.format(text_to_handle) if text_to_handle else '',
        prev_state_code_line(prev_state)
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    keyboard_if_exists = f', reply_markup={kb}' if kb else ""
    answer_content = f'await message.answer(text=\'{text_of_answer}\'{keyboard_if_exists})'
    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content,
                          handler_sample_name)


def create_state_callback_handler(imports: str, command: str, prev_state: Optional[str], text_to_handle: Optional[str],
                                  state_to_set_name: Optional[str], send_message_type: str, text_of_answer: str, kb: str) -> str:
    """Подготовка данных для генерации кода колбэк хэндлера

    Args:
        imports (str): Импорты
        command (str): Команда перехватываемая хэндлером типа /start
        prev_state (Optional[str]): Предыдущее состояние
        text_to_handle (Optional[str]): Текст перехватываемый хэндлером
        state_to_set_name (Optional[str]): Состояние к установке
        send_message_type (str): Тип отправляемого сообщения
        text_of_answer (str): Текст ответа
        kb (str): Клавиатура

    Returns:
        str: Сгенерированный код
    """

    handler_sample_name = 'callback_handler_sample.txt'
    list_of_handler_params = [
        command,
        'text = \'{0}\''.format(text_to_handle) if text_to_handle else '',
        prev_state_code_line(prev_state)
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    keyboard_if_exists = f', reply_markup={kb}' if kb else ""
    answer_content = f'await callback.message.answer(text=\'{text_of_answer}\'{keyboard_if_exists})'
    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content,
                          handler_sample_name)
