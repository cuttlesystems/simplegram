import subprocess
from pathlib import Path
from subprocess import run

import venv

from compiling_transl_ui_rc import compile_translations, compile_ui_forms, compile_rc_files
from python_venv_execs_paths import get_current_os, get_venv_python_path, get_executable_path_from_venv
from python_venv_execs_paths import get_venv_dir


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
    result = get_executable_path_from_venv('pyinstaller.exe', 'pyinstaller')
    return result


if __name__ == '__main__':
    current_os = get_current_os()
    print('current os is: {current_os}'.format(current_os=current_os))

    venv_dir = get_venv_dir()
    create_venv(venv_dir)

    compile_translations()
    compile_ui_forms()
    compile_rc_files()

    # непосредственный запуск процесса создания исполняемого файла приложения 'simple_gram' через PyInstaller
    subprocess.run([pyinstaller_exe_path(), 'start_constructor.spec', '-y'])