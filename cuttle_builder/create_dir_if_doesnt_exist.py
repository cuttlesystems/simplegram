from pathlib import Path


def create_dir_if_it_doesnt_exist(directory: Path) -> None:
    """
    Создает директорию если её не существует

    Args:
        directory (Path): путь к директории

    """
    directory.mkdir(exist_ok=True, parents=True)
