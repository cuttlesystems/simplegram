"""
модуль, необходимый для компиляции переводов, ui-файлов и файлов ресурсов '.rc'
    в ходе выполнения скрипта 'build_executable.py' по созданию исполняемого файла приложения 'simple_gram',
    а также используемый при запуске приложения
"""

import glob
import os
import subprocess

from subprocess import run

from python_venv_execs_paths import get_script_dir, get_executable_path_from_venv

from pathlib import Path

import typing


def pyside6_lrelease_exe_path() -> Path:
    """
    define function to determine the 'pyside6-lrelease' executable file's path
    Returns: путь к исполняемому файлу 'pyside6-lrelease' в созданном виртуальном окружении

    """
    result = get_executable_path_from_venv('pyside6-lrelease.exe', 'pyside6-lrelease')
    return result


def pyside6_uic_exe_path() -> Path:
    """
    define function to determine the 'pyside6-uic' executable file's path
    Returns: путь к исполняемому файлу 'pyside6-uic' в созданном виртуальном окружении

    """
    result = get_executable_path_from_venv('pyside6-uic.exe', 'pyside6-uic')
    return result


def compile_translations():
    """
    компилирование файлов переводов перед запуском процесса создания исполняемого файла приложения 'simple_gram'
    Returns: генерируются файлы переводов '*.qm' по пути
            'D:/Git Repos/tg_bot_constructor/simple_gram_desktop/constructor_app/translations/bot_constructor_*.qm'

    """
    ts_files_path = get_script_dir() / '..' / '..' / 'simple_gram_desktop' / 'constructor_app' / 'translations'
    print(f'get_script_dir: ', get_script_dir())

    localizations = list(ts_files_path.glob('**/*_man_*.ts'))
    print(f'\ntranslation files path: ', ts_files_path)
    print(f'Файлы локализаций: ', localizations)
    # localizations = ['en_US.ts', 'kk_KZ.ts', 'ru_RU.ts']

    # компилирование файлов переводов перед запуском процесса создания исполняемого файла приложения 'simple_gram'
    for localization in localizations:
        # print(f'localization: ', str(localization))
        # print(f'split(localization): ', str(localization).split('_man_'))
        # subprocess.run([pyside6_lrelease_exe_path(), ts_files_path / ('bot_constructor_man_' + 'en_US.ts'),
        #             ts_files_path / 'bot_constructor_en_US.ts', '-qm', 'bot_constructor_en_US.qm'])
        # subprocess.run
        localization_norm_path = Path(os.path.normpath(localization))
        print(f'\nlocalization: ', localization)
        print(f'localization_norm_path: ', localization_norm_path)

        # localization_norm_path.name
        # localization_without_man = str(localization_norm_path).split('_man_')[0] + '_' + str(localization_norm_path).split('_man_')[1]
        localization_without_man = localization_norm_path.parent / \
                                   str(localization_norm_path.name).replace('_man_', '_')
        print(f'localization_without_man: ', localization_without_man)
        # qm_file_name = str(localization_norm_path).split('_man_')[1].split('.')[0] + '.qm'
        qm_file_name = str(localization_without_man).replace('.ts', '.qm')
        print(f'qm_file_name: ', qm_file_name)

        subprocess.run(
            [
                pyside6_lrelease_exe_path(),
                ts_files_path / localization_norm_path,
                localization_without_man,
                '-qm',
                qm_file_name
            ]
        )


# def compile_ui_forms():
#     """
#     компилирование файлов ui-форм перед запуском процесса создания исполняемого файла приложения 'simple_gram'
#     Returns: генерируются файлы переводов '*.qm' по пути
#             'D:\Git Repos\tg_bot_constructor\simple_gram_desktop\constructor_app\translations\bot_constructor_*.qm'
#
#     """
#     ui_files_path = get_script_dir() / '..' / '..' / 'simple_gram_desktop' / 'constructor_app' / 'widgets'
#     print(f'get_script_dir: ', get_script_dir())
#
#     localizations = list(ui_files_path.glob('**/*.ui'))
#     print(f'translation files path: ', ui_files_path)
#     print(f'Файлы локализаций: ', localizations)
# localizations = ['en_US.ts', 'kk_KZ.ts', 'ru_RU.ts']

# # компилирование файлов ui-форм перед запуском процесса создания исполняемого файла приложения 'simple_gram'
# for localization in localizations:
#     # print(f'localization: ', str(localization))
#     # print(f'split(localization): ', str(localization).split('_man_'))
#     # subprocess.run([pyside6_lrelease_exe_path(), ts_files_path / ('bot_constructor_man_' + 'en_US.ts'),
#     #             ts_files_path / 'bot_constructor_en_US.ts', '-qm', 'bot_constructor_en_US.qm'])
#     # subprocess.run
#     localization_norm_path = Path(os.path.normpath(localization))
#     print(f'localization: ', localization)
#     print(f'localization_norm_path: ', localization_norm_path)
#
#     # localization_norm_path.name
#     # localization_without_man = str(localization_norm_path).split('_man_')[0] + '_' + str(localization_norm_path).split('_man_')[1]
#     localization_without_man = localization_norm_path.parent / \
#                                str(localization_norm_path.name).replace('_man_', '_')
#     print(f'localization_without_man: ', localization_without_man)
#     # qm_file_name = str(localization_norm_path).split('_man_')[1].split('.')[0] + '.qm'
#     qm_file_name = str(localization_without_man).replace('.ts', '.qm')
#     print(f'qm_file_name: ', qm_file_name)
#
#     subprocess.run(
#         [
#             pyside6_lrelease_exe_path(),
#             ts_files_path / localization_norm_path,
#             localization_without_man,
#             '-qm',
#             qm_file_name
#         ]
#     )


def name_ui_to_ui_py(name: str) -> str:
    path = Path(name)
    directory = path.parent
    filename: str = 'ui_' + path.name
    ui_path = directory / filename
    ui_py_path = ui_path.with_suffix('.py')
    return str(ui_py_path)


def compile_ui_file(ui_name: str):
    ui_py_name = name_ui_to_ui_py(ui_name)
    # run_string = 'venv\\Scripts\\pyside6-uic "{input_name}" -o "{out_name}"'.format(
    #         input_name=ui_name,
    #         out_name=ui_py_name
    #     )
    # print(run_string)
    # os.system(
    #     run_string
    # )
    #
    subprocess.run(
        [
            pyside6_uic_exe_path(),
            ui_name,
            '-o',
            ui_py_name
        ]
    )


def search_ui_files(search_dir: str) -> typing.List[Path]:
    search_dir_path = Path(search_dir)
    files = search_dir_path.glob('**/*.ui')
    files_list = list(files)
    return files_list


def compile_ui_forms():
    """
    компилирование файлов ui-форм перед запуском процесса создания исполняемого файла приложения 'simple_gram'
    Returns: генерируются файлы ui-форм в директориях
        'D:/Git Repos/tg_bot_constructor/simple_gram_desktop/constructor_app/widgets/ui_*_form.py' и
        'D:/Git Repos/tg_bot_constructor/simple_gram_desktop/constructor_app/widgets/bot_editor/ui_*_form.py'

    """
    simple_gram_desktop_project_path = os.path.normpath(get_script_dir() / '..' / '..' / 'simple_gram_desktop')
    search_dirs = [
        Path(simple_gram_desktop_project_path) / 'common',
        Path(simple_gram_desktop_project_path) / 'constructor_app',
        Path(simple_gram_desktop_project_path) / 'utils'
    ]
    print(f'\nДиректории поиска файлов ui-форм: ', search_dirs)
    ui_files = []
    ui_files_counter = 0

    for search_dir in search_dirs:
        ui_files.extend(search_ui_files(str(search_dir)))
    print(f'Список ui-файлов: ', ui_files)
    for ui_file in ui_files:
        ui_files_counter += 1
        compile_ui_file(str(ui_file))
    print(f'\nКомпиляция файлов ui-форм выполнена, скомпилировано', ui_files_counter, 'файлов')
