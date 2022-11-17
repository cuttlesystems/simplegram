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
        keyboard_directory = str(
            Path(bot_directory) / 'keyboards' / f'{keyboard_name}.py')

        init_directory = str(
            Path(bot_directory) / 'keyboards' / '__init__.py')

        self.create_file(keyboard_directory, keyboard_code,
                         init_directory,
                         f'\nfrom .{keyboard_name} import {keyboard_name}')

    def create_file_handler(self, bot_directory: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package

        Args:
            bot_directory (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        handler_directory = str(
            Path(bot_directory) / 'handlers' / f'get_{name}.py')

        init_directory = str(
            Path(bot_directory) / 'handlers' / '__init__.py')

        self.create_file(handler_directory, code, init_directory,
                         f'from .get_{name} import dp\n')

    def create_file_state(self, bot_directory: str, code) -> None:
        """create file in specific directory, contains states class and register this class in the package

        Args:
            bot_directory (str): name of bot
            code (str): code of state
        """
        handler_directory = str(
            Path(bot_directory) / 'state' / 'states.py')

        init_directory = str(
            Path(bot_directory) / 'state' / '__init__.py')

        self.create_file(handler_directory, code,
                         init_directory, 'from .states import States')

    def create_config_file(self, bot_directory, code):
        config_directory = str(
            Path(bot_directory) / 'data' / 'config.py')

        self.create_file(config_directory, code)
