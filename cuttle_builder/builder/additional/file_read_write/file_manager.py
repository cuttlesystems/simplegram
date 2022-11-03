import shutil
from distutils.dir_util import copy_tree
from abc import ABC, abstractmethod

class FileManager(ABC):
    def __init__(self) -> None:
        pass
    
    # add into directory file, that contains generated code
    def write_file(self, dir, code):
        f = open(dir, "a")
        f.seek(0,0)
        f.write(code)
        f.close()

    # add into init files names of new units to register generated code (dir - init directory, code - import of unit)
    def write_into_init(self, dir, code):
        with open(dir, 'r+') as file:
            file_data = file.read()
            file.seek(0, 0)
            print(code + file_data)
            file.write(code + file_data)
            # file.close()

    # create and register new unit of telegram bot
    def create_file(self, file_path, code, init_path, import_path):
        self.write_file(file_path, code)
        self.write_into_init(init_path, import_path)

    # place, where we store the bot (doesn't work if call outside of this file)
    def get_dir_name(self, bot_id: int) -> str:
        return '../bot_{0}'.format(bot_id)
    
    # delete directory, to prevent writing file over exist file
    def delete_dir(self, dir_name: str) -> None:
        try:
            shutil.rmtree(dir_name)
        except FileNotFoundError:
            pass 
        except Exception as e:
            print(e)
    
    # get template of bot and copy in upper directory with id of bot
    def get_template(self, bot_id: int) -> str:
        dir_name = self.get_dir_name(bot_id)
        self.delete_dir(dir_name)
        copy_tree('bot', dir_name)
        return dir_name