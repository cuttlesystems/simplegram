from builder.additional.file_read_write.write_file import write_file, write_into_init

def create_file_handler(name, code):
    write_file(f'bot/handlers/get_{name}.py', code)
    write_into_init(f'bot/handlers/__init__.py', f'from .get_{name} import dp\n')


def create_file_keyboard(keyboard_name, keyboard):
    write_file(f'bot/keyboards/{keyboard_name}.py', keyboard)
    write_into_init(f'bot/keyboards/__init__.py', f'\nfrom .{keyboard_name} import {keyboard_name}')