from pathlib import Path

from b_logic.data_objects import HandlerInit
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
        self.write_file(keyboard_code_file, keyboard_code)
        return f'\nfrom .{keyboard_name} import {keyboard_name}'

    def create_keyboard_file_init(self, bot_directory: str, keyboard_name: str):
        import_code = f'\nfrom .{keyboard_name} import {keyboard_name}'
        keyboard_init_file = str(
            Path(bot_directory) / 'keyboards' / '__init__.py')
        self.write_into_init(keyboard_init_file, import_code)

    def create_file_handler(self, bot_directory: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package

        Args:
            bot_directory (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        handler_code_file = str(
            Path(bot_directory) / 'handlers' / f'get_{name}.py')
        self.write_file(handler_code_file, code)

    def create_handler_file_init(self, bot_directory: str, name: str):
        import_code = f'from .get_{name} import dp\n'
        handler_init_file = str(
            Path(bot_directory) / 'handlers' / '__init__.py')
        self.write_into_init(handler_init_file, import_code)

    def create_state_file(self, bot_directory: str, code: str) -> None:
        """create file in specific directory, contains states class and register this class in the package

        Args:
            bot_directory (str): name of bot
            code (str): code of state
        """
        state_code_file = str(
            Path(bot_directory) / 'state' / 'states.py')
        self.write_file(state_code_file, code)

    def create_state_file_init(self, bot_directory: str):
        import_code = 'from .states import States'
        state_init_file = str(
            Path(bot_directory) / 'state' / '__init__.py')
        self.write_into_init(state_init_file, import_code)

    def create_config_file(self, bot_directory, code):
        config_code_file = str(
            Path(bot_directory) / 'data' / 'config.py')

        self.create_file(config_code_file, code)

    def create_commands_file(self, bot_directory: str, code: str) -> None:
        """
        Создает файл с кодом функции для отображения команд бота

        Args:
            bot_directory (str): Корневая директория бота
            code (str): Подготовленный код(содержимое файла)
        """
        path_to_file = str(
            Path(bot_directory) / 'on_startup_commands.py')

        self.write_file(path_to_file, code)
