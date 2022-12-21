from pathlib import Path

from b_logic.data_objects import HandlerInit
from cuttle_builder.builder.additional.file_read_write.file_manager import FileManager


class APIFileCreator(FileManager):

    def __init__(self, bot_direcory: str):
        assert isinstance(bot_direcory, str)
        self._bot_directory = bot_direcory

    def create_file_keyboard(self, keyboard_name: str, keyboard_code: str):
        """create file in specific directory, contains keyboard and register this keyboard in the package

        Args:
            keyboard_name (str): name of keyboard (message_id + _kb)
            keyboard_code (str): generated code of keyboard
        """
        assert isinstance(keyboard_name, str)
        assert isinstance(keyboard_code, str)

        keyboard_code_file = str(
            Path(self._bot_directory) / 'keyboards' / f'{keyboard_name}.py')
        self.write_file(keyboard_code_file, keyboard_code)

    def create_keyboard_file_init(self, keyboard_name: str) -> None:
        assert isinstance(keyboard_name, str)

        import_code = f'\nfrom .{keyboard_name} import {keyboard_name}'
        keyboard_init_file = str(
            Path(self._bot_directory) / 'keyboards' / '__init__.py')
        self.write_into_init(keyboard_init_file, import_code)

    def create_file_handler(self, name: str, code: str) -> None:
        """create file in specific directory, contains handler and register this handler in the package

        Args:
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        assert isinstance(name, str)
        assert isinstance(code, str)

        handler_code_file = str(
            Path(self._bot_directory) / 'handlers' / f'get_{name}.py')
        self.write_file(handler_code_file, code)

    def create_handler_file_init(self, name: str) -> None:
        assert isinstance(name, str)

        import_code = f'from .get_{name} import dp\n'
        handler_init_file = str(
            Path(self._bot_directory) / 'handlers' / '__init__.py')
        self.write_into_init(handler_init_file, import_code)

    def create_state_file(self, code: str) -> None:
        """create file in specific directory, contains states class and register this class in the package

        Args:
            code (str): code of state
        """
        assert isinstance(code, str)

        state_code_file = str(
            Path(self._bot_directory) / 'state' / 'states.py')
        self.write_file(state_code_file, code)

    def create_state_file_init(self) -> None:
        import_code = 'from .states import States'
        state_init_file = str(
            Path(self._bot_directory) / 'state' / '__init__.py')
        self.write_into_init(state_init_file, import_code)

    def create_config_file(self, code) -> None:
        assert isinstance(code, str)

        config_code_file = str(
            Path(self._bot_directory) / 'data' / 'config.py')
        self.create_file(config_code_file, code)

    def create_commands_file(self, code: str) -> None:
        """
        Создает файл с кодом функции для отображения команд бота

        Args:
            code (str): Подготовленный код(содержимое файла)
        """
        assert isinstance(code, str)

        path_to_file = str(
            Path(self._bot_directory) / 'on_startup_commands.py')
        self.write_file(path_to_file, code)
