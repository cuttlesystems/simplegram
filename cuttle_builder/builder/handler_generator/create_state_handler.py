# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler

def create_state_handler(imports, type_, prev_state, prev_state_text, curr_state, send_message, text, kb):
    send_method = f'await message.answer(text=\'{text}\', {"reply_markup="+kb if kb else ""})'
    message_body = 'await States.{0}.set()'.format(curr_state)
    # additional_function = 'await States.{0}.set()'.format(curr_state)
    # content_type = 'lambda message: message.text == \'{0}\', state=States.{1}'.format(prev_state_text, prev_state) if not type_ else type_
    content_type = 'lambda message: message.text == \'{0}\', state=States.{1}'.format(prev_state_text, prev_state) if prev_state else type_
    return create_handler(imports=imports, 
                        type_= content_type,
                        name = f'{curr_state}',
                        method_body = message_body,
                        send_message = send_method
                        )
