from pathlib import Path


def get_project_root_dir() -> Path:
    """
    Возвращает полный путь до корневой директории проекта.

    Returns: Полный путь до корневой директории проекта.
    """
    print('Don not use get_project_root_dir from common_utils. Refactor')
    return Path(__file__).resolve().parent.parent


def get_project_root_dir_name() -> str:
    """
    Возвращает имя корневой директории проекта.

    Returns: Имя корневой директории проекта.
    """
    print('Don not use get_project_root_dir_name from common_utils. Refactor')
    root_path = str(get_project_root_dir())
    root_path_list = root_path.split('/')
    return root_path_list[-1]
