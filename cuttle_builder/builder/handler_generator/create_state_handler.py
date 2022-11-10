# method to create handler, based on state and text
from cuttle_builder.builder.handler_generator.create_handler import create_handler

def command_to_quotes(line: str) -> str:
    return '\'{0}\''.format(line)

def create_state_handler(imports, type_, prev_state, prev_state_text, curr_state, send_message, text, kb):
    send_method = f'await message.answer(text=\'{text}\', {"reply_markup="+kb if kb else ""})'
    message_body = 'await States.{0}.set()'.format(curr_state) if curr_state else ''
    # additional_function = 'await States.{0}.set()'.format(curr_state)
    # content_type = 'lambda message: message.text == \'{0}\', state=States.{1}'.format(prev_state_text, prev_state) if not type_ else type_
    # prev_state_text = command_to_quotes(prev_state_text)

    lambda_mes = ''

    list_of_content_type = [
        type_,
        'lambda message: message.text == \'{0}\''.format(prev_state_text) if prev_state_text else '',
        'state=States.{0}'.format(prev_state) if prev_state != '*' and prev_state else 'state={0}'.format(command_to_quotes(prev_state)) if prev_state else prev_state
    ]

    content_type = ', '.join(element for element in list_of_content_type if element)
    print(prev_state)
    print(prev_state_text)
    print(curr_state)
    print()
    # content_type = 'lambda message: message.text == \'{0}\', state=States.{1}'.format(prev_state_text, prev_state) if prev_state else type_
    return create_handler(imports=imports, 
                        type_= content_type,
                        name = f'{curr_state}',
                        method_body = message_body,
                        send_message = send_method
                        )
