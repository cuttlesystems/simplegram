import os
import subprocess

import sys
import venv
from pathlib import Path
from subprocess import run

from python_and_venv_path import OsClass, get_current_os, get_venv_python_path, get_building_dir


# функция создания виртуального окружения с установкой пакета 'pip', последующим его обновлением и
#  установкой требуемых пакетов из файла 'requirements.txt'
def create_venv(venv_dir: Path):
    assert isinstance(venv_dir, Path)
    print(f'Current OS: ', get_current_os())

    print(f'venv_dir path: ', venv_dir)
    print(f'Current OS related directory path: ', venv_dir.parent)

    if not venv_dir.parent.exists():
        venv_dir.parent.mkdir(exist_ok=True)
        venv.create(venv_dir, with_pip=True)

    run([get_venv_python_path(venv_dir), '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([get_venv_python_path(venv_dir), '-m', 'pip', 'install', '-r', 'requirements.txt'])


# define function to determine the PyInstaller executable file's path
def pyinstaller_exe_path() -> Path:
    current_os = get_current_os()
    scripts_bin_path = get_venv_python_path(venv_dir).parent
    if current_os == OsClass.WINDOWS_CLASS:
        result = scripts_bin_path / 'pyinstaller.exe'
    elif current_os == OsClass.LINUX_CLASS:
        result = scripts_bin_path / 'pyinstaller'
    else:
        raise NotImplementedError('Unsupported os')
    print(f'scripts (or bin) path: ', scripts_bin_path)
    print(f'PyInstaller executable path: ', result)
    return result


if __name__ == '__main__':
    # print('get_script_dir(): ', get_script_dir())


    current_os = get_current_os()
    print('current os is: {current_os}'.format(current_os=current_os))

    venv_dir = get_building_dir() / 'venv'
    create_venv(venv_dir)

# непосредственный запуск процесса создания исполняемого файла приложения 'simple_gram' через PyInstaller
    subprocess.run([pyinstaller_exe_path(), 'start_constructor.spec', '-y'])