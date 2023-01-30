import shutil

from pathlib import Path
from typing import Optional, List

from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH


class FileManager:
    _FROM_BEGINNING = 0

    def __init__(self) -> None:
        pass

    def create_bot_directory(self, directory: str) -> str:
        """ get template of bot and copy in upper directory with id of bot (doesn't work if call outside of cuttle_builder directory)

        Args:
            directory (str): directory
        Returns:
            str: directory path
        """
        self.delete_dir(directory)
        bot_sample_dirs_tree = CUTTLE_BUILDER_PATH / 'bot'
        shutil.copytree(str(bot_sample_dirs_tree), directory)
        return directory

    def delete_bot_by_id(self, bot_id: int) -> None:
        """ delete directory created for bot

        Args:
            bot_id (int): id of bot
        """
        directory = self._get_dir(bot_id)
        self.delete_dir(directory)

    def delete_dir(self, directory: str) -> None:
        """delete directory, to prevent writing file over exist file

        Args:
            directory (str): directory path
        """
        try:
            shutil.rmtree(directory)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)

    def read_file(self, directory: str) -> str:
        with open(directory, 'r') as file:
            return file.read()

    def read_file_by_line(self, directory: str) -> List[str]:
        with open(directory, 'r') as file:
            return file.read().split('\n')

    def _get_dir(self, bot_id: int) -> str:
        """generate path, where bot is store (doesn't work if call outside of cuttle_builder directory)

        Args:
            bot_id (int): id of bot

        Returns:
            str: file path
        """
        return 'bot_{0}'.format(bot_id)

    def _write_file_insert(self, directory: str, code: str) -> None:
        """add into directory file, that contains generated code

        Args:
            directory:
            code (_type_): generated code
        """
        with open(directory, 'a', encoding='utf-8') as f:
            f.write(code)

    def _write_file_owerwrite(self, directory: str, code: str) -> None:
        """add into directory file, that contains generated code

        Args:
            directory:
            code (_type_): generated code
        """
        with open(directory, 'w', encoding='utf-8') as f:
            f.write(code)

    def _write_into_init(self, directory: str, code: str) -> None:
        """add into init files names of new units to register generated code (dir - init directory, code - import of unit)

        Args:
            directory:
            dir (_type_): directory path
            code (_type_): generated code (import insdide init)
        """
        with open(directory, 'r+') as file:
            file_data = file.read()
            file.seek(0, self._FROM_BEGINNING)
            file.write(code + file_data)
