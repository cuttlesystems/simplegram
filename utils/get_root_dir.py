from pathlib import Path


def get_project_root_dir() -> Path:
    """
    Возвращает полный путь до корневой директории проекта.

    Returns: Полный путь до корневой директории проекта.
    """
    return Path(__file__).resolve().parent.parent


def get_project_root_dir_name() -> str:
    """
    Возвращает имя корневой директории проекта.

    Returns: Имя корневой директории проекта.
    """
    root_path = str(get_project_root_dir())
    root_path_list = root_path.split('/')
    return root_path_list[-1]
