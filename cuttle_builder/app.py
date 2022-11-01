from builder import write_file, state_generator, write_into_init, create_reply_keyboard, create_state_handler, create_keyboard_array, find_previous_messages, create_file_handler, create_file_keyboard

messages = [
    {
        'id': 'asdf',
        'text': 'asdftext',
        'photo': None,
        'video': None,
        'file': None
    },
    {
        'id': 'qwer',
        'text': 'qwertext',
        'photo': None,
        'video': None,
        'file': None
    },
    {
        'id': 'zxcv',
        'text': 'zxcvtext',
        'photo': None,
        'video': None,
        'file': None
    },
    {
        'id': 'qaz',
        'text': 'qaztext',
        'photo': None,
        'video': None,
        'file': None
    },    
    {
        'id': 'wsx',
        'text': 'wsxtext',
        'photo': None,
        'video': None,
        'file': None
    },    
]

variants = [
    {
        'text': 'asdf_to_zxcv',
        'current_id': 'asdf',
        'next_id': 'zxcv'
    },
    {
        'text': 'asdf_to_qwer',
        'current_id': 'asdf',
        'next_id': 'qwer'
    },
    {
        'text': 'asdf_to_qaz',
        'current_id': 'asdf',
        'next_id': 'qaz'
    },
    {
        'text': 'zxcv_wsx',
        'current_id': 'zxcv',
        'next_id': 'wsx'
    },
    {
        'text': 'qwer_to_wsx',
        'current_id': 'qwer',
        'next_id': 'wsx'
    }
]

# create_state_handler take 1 more positional argument send_method, it needs to generate method to send message
for message in messages:
    name = message['id']
    buttons = create_keyboard_array(name, variants)
    keyboard_code = create_reply_keyboard(name, buttons) if buttons else ''
    keyboard_name = name + '_kb' if keyboard_code else ''
    imp = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''
    previouses = find_previous_messages(name, variants)

    for previous in previouses:
        if keyboard_name:
            create_file_keyboard(keyboard_name, keyboard_code)
        code = create_state_handler(imp, previous['current_id'], previous['text'], name, 'photo', message['text'], keyboard_name)
        create_file_handler(name, code)
    if not previouses:
        if keyboard_name:
            create_file_keyboard(keyboard_name, keyboard_code)
        code = create_state_handler(imp, '', '', name, 'photo', message['text'], keyboard_name)
        create_file_handler(name, code)