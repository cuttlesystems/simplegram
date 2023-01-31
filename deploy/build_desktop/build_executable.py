import os
import subprocess

import sys
import venv
from pathlib import Path
from subprocess import run

from python_and_venv_path import OsClass, get_current_os, get_script_dir, get_venv_python_path, get_building_dir
import glob


def create_venv(venv_dir: Path):
    """
    функция создания виртуального окружения с установкой пакета 'pip', последующим его обновлением и
    установкой требуемых пакетов из файла 'requirements.txt'
    Args:
        venv_dir: путь к папке виртуального окружения

    Returns: созданное виртуальное окружение с установленным и обновлённым пакетом 'pip',
    а также установленными требуемыми пакетами из файла 'requirements.txt'

    """
    assert isinstance(venv_dir, Path)
    print(f'Current OS: ', get_current_os())

    print(f'venv_dir path: ', venv_dir)
    print(f'Current OS related directory path: ', venv_dir.parent)

    if not venv_dir.parent.exists():
        venv_dir.parent.mkdir(exist_ok=True)
        venv.create(venv_dir, with_pip=True)

    run([get_venv_python_path(venv_dir), '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([get_venv_python_path(venv_dir), '-m', 'pip', 'install', '-r', 'requirements.txt'])


def pyinstaller_exe_path() -> Path:
    """
    define function to determine the PyInstaller executable file's path
    Returns: путь к исполняемому файлу 'PyInstaller' в созданном виртуальном окружении

    """
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


def pyside6_lrelease_exe_path() -> Path:
    """
    define function to determine the 'pyside6-lrelease' executable file's path
    Returns: путь к исполняемому файлу 'pyside6-lrelease' в созданном виртуальном окружении

    """
    current_os = get_current_os()
    scripts_bin_path = get_venv_python_path(venv_dir).parent
    if current_os == OsClass.WINDOWS_CLASS:
        result = scripts_bin_path / 'pyside6-lrelease.exe'
    elif current_os == OsClass.LINUX_CLASS:
        result = scripts_bin_path / 'pyside6-lrelease'
    else:
        raise NotImplementedError('Unsupported os')
    print(f'scripts (or bin) path: ', scripts_bin_path)
    print(f'pyside6-lrelease executable path: ', result)
    return result


if __name__ == '__main__':
    current_os = get_current_os()
    print('current os is: {current_os}'.format(current_os=current_os))

    venv_dir = get_building_dir() / 'venv'
    create_venv(venv_dir)

    ts_files_path = get_script_dir() / '..' / '..' / 'simple_gram_desktop' / 'constructor_app' / 'translations'

    localizations = list(ts_files_path.glob ('**/*.ts'))
    print(f'translation files path: ', ts_files_path)
    print(f'Файлы локализаций: ', localizations)
    # localizations = ['en_US.ts', 'kk_KZ.ts', 'ru_RU.ts']

# компилирование файлов переводов перед запуском процесса создания исполняемого файла приложения 'simple_gram'
    for i in localizations:
        subprocess.run([pyside6_lrelease_exe_path(), ts_files_path / 'bot_constructor_man_en_US.ts',
                    ts_files_path / 'bot_constructor_en_US.ts', '-qm', 'bot_constructor_en_US.qm'])

# непосредственный запуск процесса создания исполняемого файла приложения 'simple_gram' через PyInstaller
    subprocess.run([pyinstaller_exe_path(), 'start_constructor.spec', '-y'])