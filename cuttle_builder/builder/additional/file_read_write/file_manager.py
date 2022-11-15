import shutil
# from distutils.dir_util import copy_tree
import os

from pathlib import Path
from typing import Optional


class FileManager:
    def __init__(self) -> None:
        pass

    def read_file(self, directory: str):
        with open(directory, 'r') as file:
            return file.read()

    def read_file_by_line(self, directory: str):
        with open(directory, 'r') as file:
            return file.read().split('\n')
    def rewrite_file(self, directory: str, code: str) -> None:
        """add into directory file, that contains generated code

        Args:
            dir (_type_): directory path
            code (_type_): generated code
        """
        self.write_file(directory, code, 'a')
        # with open(directory, "a", encoding='utf-8') as f:
        #     f.seek(0,0)
        #     f.write(code)
        #     f.close()
        #

    def write_new_file(self, directory: str, code: str) -> None:
        """add into directory file, that contains generated code

        Args:
            dir (_type_): directory path
            code (_type_): generated code
        """
        self.write_file(directory, code, 'w')

    def write_file(self, directory: str, code: str) -> None:
        """add into directory file, that contains generated code

        Args:
            dir (_type_): directory path
            code (_type_): generated code
        """

        with open(directory, 'a', encoding='utf-8') as f:
            f.seek(0,0)
            f.write(code)
            f.close()

    def write_into_init(self, directory: str, code: str) -> None:
        """add into init files names of new units to register generated code (dir - init directory, code - import of unit)

        Args:
            dir (_type_): directory path
            code (_type_): generated code (import insdide init)
        """
        with open(directory, 'r+') as file:
            file_data = file.read()
            file.seek(0, 0)
            file.write(code + file_data)
            # file.close()

    def create_file(self, file_path: str, code: str, init_path: Optional[str] = None, import_code: Optional[str] = None) -> None:
        """create and register new unit of telegram bot

        Args:
            file_path (_type_): file path
            code (_type_): generated code
            init_path (_type_): init file path
            import_code (_type_): generated code (import inside init)
            flag (_type_): write new file or rewrite exist file
        """
        self.write_file(file_path, code)
        if init_path is not None and import_code is not None:
            self.write_into_init(init_path, import_code)

    def get_dir(self, bot_id: int) -> str:
        """generate path, where bot is store (doesn't work if call outside of cuttle_builder directory)

        Args:
            bot_id (int): id of bot

        Returns:
            str: file path
        """
        return 'bot_{0}'.format(bot_id)

    # 
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

    def create_bot_directory(self, bot_id: int) -> str:
        """ get template of bot and copy in upper directory with id of bot (doesn't work if call outside of cuttle_builder directory)

        Args:
            bot_id (int): id of bot

        Returns:
            str: directory path
        """
        directory = self.get_dir(bot_id)
        self.delete_bot_by_id(bot_id)
        bot_dir = Path(__file__).parent.parent.parent.parent / 'bot'
        shutil.copytree(str(bot_dir), directory)
        return directory

    def delete_bot_by_id(self, bot_id: int) -> None:
        """ delete directory created for bot

                Args:
                    bot_id (int): id of bot
                """
        directory = self.get_dir(bot_id)
        self.delete_dir(directory)