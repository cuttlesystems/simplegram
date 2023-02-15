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


def write_specfileconf(app_type: ApplicationTypeEnum):
    """
    write 'application_type' into 'specfileconf.json' file
    Args:
        app_type: ApplicationTypeEnum

    Returns: 'specfileconf.json' file with 'simple_gram' application type as content

    """
    assert isinstance(app_type, ApplicationTypeEnum)
    params = {
        'application_type': app_type.value
    }
    with open('specfileconf.json', 'wt') as conffile:
        json.dump(params, conffile)
    print(f'\n--- The application type was written into \'specfileconf.json\', content: \n      {params} ---')


def get_start_constructor_spec_file_path() -> Path:
    """
    define function to get 'start_constructor.spec' file path
    :return:
        'start_constructor.spec' file path

    """
    start_constructor_spec_file_name = 'start_constructor.spec'
    # путь для проверки существования файла 'start_constructor.spec'
    #  (с конфигурационными данными для сборки исполняемого файла приложения с помощью PyInstaller)
    #  в директории "..\deploy\build_desktop"
    search_dir_path = Path(__file__).parent
    start_constructor_spec_file_path = search_dir_path / start_constructor_spec_file_name
    print(f'\nDirectory for \'start_constructor.spec\' file search path:\n{search_dir_path}')
    print(f'\n\'start_constructor.spec\' file search path:\n{start_constructor_spec_file_path}\n')
    return start_constructor_spec_file_path


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

    # write 'application_type' into 'specfileconf.json' file
    write_specfileconf(app_type)

    # непосредственный запуск процесса создания исполняемого файла приложения 'simple_gram' через PyInstaller
    print('\n--- building app executable started ---')
    subprocess.run([pyinstaller_exe_path(), get_start_constructor_spec_file_path(), '-y'])
    print('\n--- building app executable ended ---\n\n')
