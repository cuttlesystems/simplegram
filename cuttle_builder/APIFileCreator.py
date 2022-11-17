from pathlib import Path

from cuttle_builder.builder.additional.file_read_write.file_manager import FileManager


class APIFileCreator(FileManager):

    def create_file_keyboard(self, bot_directory: str, keyboard_name: str, keyboard_code: str):
        """create file in specific directory, contains keyboard and register this keyboard in the package

        Args:
            bot_directory (str): name of bot
            keyboard_name (str): name of keyboard (message_id + _kb)
            keyboard_code (str): generated code of keyboard
        """
        keyboard_code_file = str(
            Path(bot_directory) / 'keyboards' / f'{keyboard_name}.py')

        keyboard_init_file = str(
            Path(bot_directory) / 'keyboards' / '__init__.py')

        self.create_file(keyboard_code_file, keyboard_code,
                         keyboard_init_file,
                         f'\nfrom .{keyboard_name} import {keyboard_name}')

    def create_file_handler(self, bot_directory: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package

        Args:
            bot_directory (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        handler_code_file = str(
            Path(bot_directory) / 'handlers' / f'get_{name}.py')

        handler_init_file = str(
            Path(bot_directory) / 'handlers' / '__init__.py')

        self.create_file(handler_code_file, code, handler_init_file,
                         f'from .get_{name} import dp\n')

    def create_file_state(self, bot_directory: str, code) -> None:
        """create file in specific directory, contains states class and register this class in the package

        Args:
            bot_directory (str): name of bot
            code (str): code of state
        """
        state_code_file = str(
            Path(bot_directory) / 'state' / 'states.py')

        state_init_file = str(
            Path(bot_directory) / 'state' / '__init__.py')

        self.create_file(state_code_file, code,
                         state_init_file, 'from .states import States')

    def create_config_file(self, bot_directory, code):
        config_code_file = str(
            Path(bot_directory) / 'data' / 'config.py')

        self.create_file(config_code_file, code)
