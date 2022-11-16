# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler
from cuttle_builder.builder.additional.helpers.string_in_quotes import string_to_quotes


def create_state_handler(imports, type_, prev_state, prev_state_text, curr_state, send_message_type, text, kb):
    send_method = f'await message.answer(text=\'{text}\'{", reply_markup=" + kb if kb else ""})'
    message_body = 'await States.{0}.set()'.format(curr_state) if curr_state else ''
    list_of_content_type = [
        type_,
        'lambda message: message.text == \'{0}\''.format(prev_state_text) if prev_state_text else '',
        'state=States.{0}'.format(prev_state) if prev_state != '*' and prev_state is not None else 'state={0}'.format(
            string_to_quotes(prev_state)) if prev_state else prev_state
    ]
    content_type = ', '.join(element for element in list_of_content_type if element)
    return create_handler(imports=imports,
                          content_type=content_type,
                          name=curr_state,
                          method_body=message_body,
                          send_method=send_method
                          )
