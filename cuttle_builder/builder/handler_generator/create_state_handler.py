# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler


def prev_state_code_line(prev_state):
    if prev_state == '*':
        return 'state=\'*\''
    elif prev_state is not None:
        return 'state=States.{0}'.format(prev_state)
    return ''


def create_state_message_handler(imports, type_, prev_state, text_to_handle, state_to_set_name,
                                 send_message_type, text_of_answer, kb):
    handler_sample_name = 'message_handler_sample.txt'
    list_of_handler_params = [
        type_,
        'lambda message: message.text == \'{0}\''.format(text_to_handle) if text_to_handle else '',
        prev_state_code_line(prev_state)
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    answer_content = f'await message.answer(text=\'{text_of_answer}\'{", reply_markup=" + kb if kb else ""})'
    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content,
                          handler_sample_name)


def create_state_callback_handler(imports, type_, prev_state, text_to_handle, state_to_set_name,
                                  send_message_type, text_of_answer, kb):
    handler_sample_name = 'callback_handler_sample.txt'
    list_of_handler_params = [
        type_,
        'text = \'{0}\''.format(text_to_handle) if text_to_handle else '',
        prev_state_code_line(prev_state)
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    answer_content = f'await callback.message.answer(text=\'{text_of_answer}\'{", reply_markup=" + kb if kb else ""})'
    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content,
                          handler_sample_name)
