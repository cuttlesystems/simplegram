"""
модуль, используемый для проверки существования и создания виртуального окружения в каталоге 'build_desktop'
"""

from pathlib import Path
from subprocess import run

import venv

from python_venv_execs_paths import get_venv_python_path, get_venv_dir, get_project_dir


def create_venv(venv_dir: Path, requirements_file_path: Path):
    """
    функция создания виртуального окружения с установкой пакета 'pip', последующим его обновлением и
    установкой требуемых пакетов из файла 'requirements.txt'
    Args:
        venv_dir: путь к папке виртуального окружения

    Returns: созданное виртуальное окружение с установленным и обновлённым пакетом 'pip',
    а также установленными требуемыми пакетами из файла 'requirements.txt'

    """
    assert isinstance(venv_dir, Path)

    print(f'venv_dir path: ', venv_dir)
    print(f'Current OS related directory path: ', venv_dir.parent, '\n')

    if not venv_dir.exists():
        venv_dir.mkdir(exist_ok=True, parents=True)
        venv.create(venv_dir, with_pip=True)

    run([get_venv_python_path(venv_dir), '-m', 'pip', 'install', '--upgrade', 'pip'])
    run(
        [
            get_venv_python_path(venv_dir),
            '-m',
            'pip',
            'install',
            '-r',
            requirements_file_path
        ]
    )


def create_venv_in_build_desktop():
    print(f'get_venv_dir path: ', get_venv_dir())
    create_venv(get_venv_dir(), get_project_dir() / 'requirements.txt')
