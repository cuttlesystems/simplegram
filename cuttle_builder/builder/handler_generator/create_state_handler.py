# method to create handler, based on state and text

from builder.handler_generator.create_handler import create_handler

def create_state_handler_new(imports, additionals, send_methods):
    send = send_methods()
def create_state_handler(imports, prev_state, prev_state_text, curr_state, send_method, text, kb = ''):
    send_method = f'await message.answer(text=\'{text}\', {"reply_markup="+kb if kb else ""})'
    additional_function = 'await States.{0}.set()'.format(curr_state)
    return create_handler(imports=imports, 
                        type_= 'lambda message: message.text == \'{0}\', state=States.{1}'.format(prev_state_text, prev_state) if prev_state else '',
                        name = f'{curr_state}',
                        additional_function = additional_function, 
                        send_method = send_method)