import shutil
# from distutils.dir_util import copy_tree
import os

from pathlib import Path


class FileManager():
    def __init__(self) -> None:
        pass
    

    def write_file(self, dir: str, code: str) -> None:
        """add into directory file, that contains generated code

        Args:
            dir (_type_): directory path
            code (_type_): generated code
        """
        with open(dir, "a", encoding='utf-8') as f:
            f.seek(0,0)
            f.write(code)
            f.close()


    def write_into_init(self, dir: str, code: str) -> None:
        """add into init files names of new units to register generated code (dir - init directory, code - import of unit)

        Args:
            dir (_type_): directory path
            code (_type_): generated code (import insdide init)
        """
        with open(dir, 'r+') as file:
            file_data = file.read()
            file.seek(0, 0)
            file.write(code + file_data)
            # file.close()

    
    def create_file(self, file_path: str, code: str, init_path: str, import_code: str) -> None:
        """create and register new unit of telegram bot

        Args:
            file_path (_type_): file path
            code (_type_): generated code
            init_path (_type_): init file path
            import_code (_type_): generated code (import inside init)
        """
        self.write_file(file_path, code)
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
    def delete_dir(self, dir: str) -> None:
        """delete directory, to prevent writing file over exist file

        Args:
            dir (str): directory path
        """
        try:
            shutil.rmtree(dir)
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
        dir = self.get_dir(bot_id)
        self.delete_bot_by_id(bot_id)
        bot_dir = Path(__file__).parent.parent.parent.parent / 'bot'
        shutil.copytree(str(bot_dir), dir)
        return dir

    def delete_bot_by_id(self, bot_id: int) -> None:
        """ delete directory created for bot

                Args:
                    bot_id (int): id of bot
                """
        dir = self.get_dir(bot_id)
        self.delete_dir(dir)