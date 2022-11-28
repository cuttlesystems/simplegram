# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler
from cuttle_builder.builder.additional.helpers.string_in_quotes import string_to_quotes


def create_state_handler(imports, type_, prev_state, text_to_handle, state_to_set_name,
                         send_message_type, text_of_answer, kb):
    list_of_handler_params = [
        type_,
        'lambda message: message.text == \'{0}\''.format(text_to_handle) if text_to_handle else '',
        'state=States.{0}'.format(prev_state) if prev_state != '*' and prev_state is not None else 'state={0}'.format(
            string_to_quotes(prev_state)) if prev_state else prev_state
    ]
    handler_params = ', '.join(element for element in list_of_handler_params if element)
    state_to_set_content = 'await States.{state_name}.set()'.format(state_name=state_to_set_name) if state_to_set_name else ''
    answer_content = f'await message.answer(text=\'{text_of_answer}\'{", reply_markup=" + kb if kb else ""})'
    return create_handler(imports,
                          handler_params,
                          state_to_set_name,
                          state_to_set_content,
                          answer_content)
