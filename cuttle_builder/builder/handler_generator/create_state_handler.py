from builder.handler_generator.create_handler import create_handler

def create_state_handler(imports, curr_state, curr_state_text, next_state, send_method, text, kb = ''):
    send_method = f'await message.answer(text=\'{text}\', {"reply_markup="+kb if kb else ""})'
    return create_handler(imports, 'lambda message: message.text == \'{0}\', state=States.{1}'.format(curr_state_text, curr_state) if curr_state else '',f'{next_state}', 'await States.{0}.set()'.format(next_state), send_method)
