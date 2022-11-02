from builder.additional.file_read_write.write_file import write_file, write_into_init


def create_file(file_path, code, init_path, import_path):
    write_file(file_path, code)
    write_into_init(init_path, import_path)

def create_file_handler(bot_name, name, code):
    create_file(f'{bot_name}/handlers/get_{name}.py', code, f'{bot_name}/handlers/__init__.py', f'from .get_{name} import dp\n')

def create_file_keyboard(bot_name, keyboard_name, keyboard):
    create_file(f'{bot_name}/keyboards/{keyboard_name}.py', keyboard, f'{bot_name}/keyboards/__init__.py', f'\nfrom .{keyboard_name} import {keyboard_name}')


def create_file_state(bot_name, code):
    create_file(f'{bot_name}/state/states.py', code, f'{bot_name}/state/__init__.py', 'from .states import States')
    

# write_file('bot/state/states.py', state_generator([str(uuid.uuid1()).replace('-', ''),str(uuid.uuid1()).replace('-', ''),str(uuid.uuid1()).replace('-', ''),str(uuid.uuid1()).replace('-', ''),str(uuid.uuid1()).replace('-', '')]))
# write_into_init('bot/state/__init__.py', 'from .states import State')

