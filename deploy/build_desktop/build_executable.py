import subprocess
from pathlib import Path

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


if __name__ == '__main__':
    """
    вызов функции проверки существования и создания виртуального окружения в каталоге 'build_desktop'
    """
    print('\n--- check \'build_desktop\' directory for \'venv\' existance and creation if it doesn\'t exist ---\n')
    create_venv_in_build_desktop()

    compile_translations()
    compile_ui_forms()
    compile_rc_files()

    # непосредственный запуск процесса создания исполняемого файла приложения 'simple_gram' через PyInstaller
    subprocess.run([pyinstaller_exe_path(), 'start_constructor.spec', '-y'])
