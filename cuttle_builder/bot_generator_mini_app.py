import os
import typing
import tempfile
import shutil
from pathlib import Path

from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotDescription, BotMessage
from cuttle_builder.bot_generator_db import BotGeneratorDb


class BotGeneratorMiniApp(BotGeneratorDb):
    def __init__(self, bot_api: IBotApi, bot: BotDescription, bot_dir: str):
        # Определение закрытой переменной _temp_dir
        self._temp_dir = None
        super().__init__(bot_api, bot, bot_dir)

    def get_file_format(self, photo_url: str) -> str:
        """
        Возвращает формат файла.

        Args:
            photo_url (str): url файла.

        Returns:
            str: формат файла.
        """
        return Path(photo_url).suffix[1:]

    def create_directory(self) -> str:
        """
        Создает уникальную директорию для медиафайлов в /temp/ директории.

        Returns:
            str: путь к созданной директории.
        """
        directory_path = str(Path(tempfile.mkdtemp(prefix=None)))
        return directory_path

    def _preprocess_data(self, messages: typing.List[BotMessage]):
        """
        Обрабатывает данные перед генерацией.

        Args:
            messages: typing.List[BotMessage]: список сообщений BotMessage.

        """
        self._temp_dir = self.create_directory()
        for message in messages:
            if message.photo is None:
                continue
            photo_bytes = self._bot_api.get_image_data_by_url(message.photo)
            file_format = self.get_file_format(message.photo)
            file_path = str(Path(self._temp_dir) / f'{message.id}.{file_format}')
            with open(file_path, 'wb') as message_file:
                message_file.write(photo_bytes)
            message.photo = file_path
            message.photo_filename = Path(file_path).name
            message.photo_file_format = file_format

    def _after_finished(self):
        """
        Удаление медиафайлов из директории /temp/
        """
        if self._temp_dir:
            try:
                shutil.rmtree(self._temp_dir)
            except PermissionError as err:
                print(f'No permission to delete directory: {self._temp_dir}: {err}')
            except FileNotFoundError as err:
                print(f'Directory not found: {self._temp_dir}: {err}')
            except OSError as err:
                print(f'Error deleting directory {self._temp_dir}: {err}')
