import subprocess
import os
from pathlib import Path

import typing


def name_ui_to_ui_py(name: str) -> str:
    path = Path(name)
    directory = path.parent
    filename: str = 'ui_' + path.name
    ui_path = directory / filename
    ui_py_path = ui_path.with_suffix('.py')
    return str(ui_py_path)


def compile_ui_file(ui_name: str):
    ui_py_name = name_ui_to_ui_py(ui_name)
    run_string = 'venv\\Scripts\\pyside6-uic "{input_name}" -o "{out_name}"'.format(
            input_name=ui_name,
            out_name=ui_py_name
        )
    print(run_string)
    os.system(
        run_string
    )


def search_ui_files(search_dir: str) -> typing.List[Path]:
    search_dir_path = Path(search_dir)
    files = search_dir_path.glob('**/*.ui')
    files_list = list(files)
    return files_list


if __name__ == '__main__':
    search_dirs = [
        Path('.') / 'common',
        Path('.') / 'constructor_app',
        Path('.') / 'utils'
    ]
    ui_files = []
    for search_dir in search_dirs:
        ui_files.extend(search_ui_files(str(search_dir)))

    for ui_file in ui_files:
        compile_ui_file(str(ui_file))
