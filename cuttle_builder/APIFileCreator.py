from cuttle_builder.builder.additional.file_read_write.file_manager import FileManager


class APIFileCreator(FileManager):

    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        """create file in specific directory, contains keyboard and register this keyboard in the package

        Args:
            bot_name (str): name of bot
            keyboard_name (str): name of keyboard (message_id + _kb)
            keyboard_code (str): generated code of keyboard
        """
        self.create_file(f'{bot_name}/keyboards/{keyboard_name}.py', keyboard_code,
                                       f'{bot_name}/keyboards/__init__.py',
                                       f'\nfrom .{keyboard_name} import {keyboard_name}')

    def create_file_handler(self, bot_name: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package

        Args:
            bot_name (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        self.create_file(f'{bot_name}/handlers/get_{name}.py', code, f'{bot_name}/handlers/__init__.py',
                                       f'from .get_{name} import dp\n')

    def create_file_state(self, bot_name: str, code) -> None:
        """create file in specific directory, contains states class and register this class in the package

        Args:
            bot_name (str): name of bot
        """
        self.create_file(f'{bot_name}/state/states.py', code,
                                       f'{bot_name}/state/__init__.py', 'from .states import States')

    def create_config_file(self, bot_directory, code):
        self.create_file(f'{bot_directory}/data/config.py', code)