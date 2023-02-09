import json
import subprocess
from pathlib import Path

from application_type_enum import ApplicationTypeEnum
from compiling_transl_ui_rc import compile_translations, compile_ui_forms, compile_rc_files
from create_venv import create_venv_in_build_desktop
from python_venv_execs_paths import get_executable_path_from_venv


def pyinstaller_exe_path() -> Path:
    """
    define function to determine the PyInstaller executable file's path
    Returns: путь к исполняемому файлу 'PyInstaller' в созданном виртуальном окружении

    """
    result = get_executable_path_from_venv('pyinstaller.exe', 'pyinstaller')
    return result


def build_executable_app(app_type: ApplicationTypeEnum):
    """
    define function to build app executable file
    Args:
        app_type: ApplicationTypeEnum

    Returns: executable file of 'simple_gram_chamomile' or 'simple_gram_shiboken' application

    """
    assert isinstance(app_type, ApplicationTypeEnum)
    # вызов функции проверки существования и создания виртуального окружения в каталоге 'build_desktop'
    print('\n--- check \'build_desktop\' directory for \'venv\' existance and creation if it doesn\'t exist ---\n')
    create_venv_in_build_desktop()

    print('\n--- translations compilation started ---')
    compile_translations()
    print('--- translations compilation ended ---\n\n')
    print('--- ui_forms compilation started ---')
    compile_ui_forms()
    print('--- ui_forms compilation ended ---\n\n')
    print('--- resources compilation started ---')
    compile_rc_files()
    print('--- resources compilation ended ---\n\n')

    params = {
        'application_type': app_type.value
    }
    with open('specfileconf.json', 'wt') as conffile:
        json.dump(params, conffile)

    # непосредственный запуск процесса создания исполняемого файла приложения 'simple_gram' через PyInstaller
    subprocess.run([pyinstaller_exe_path(), 'start_constructor.spec', '-y'])
