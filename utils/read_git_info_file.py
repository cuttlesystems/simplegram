from pathlib import Path
import json


ROOT_DIR = Path(__file__).resolve().parent.parent


def read_info_from_file_about_commit() -> str:
    """
    Возвращает данные о текущем коммите, если файл с информацией существует.

    Returns:
        str: Данные о коммите.
    """
    result = 'Information about commit not found.'
    filename = str(ROOT_DIR / 'current_commit_info.json')
    if Path(filename).exists():
        with open(filename, 'r') as commit_info:
            commit_dict = json.load(commit_info)
            result = ('Commit hash: ' + commit_dict['commit_hash'] +
                      ', Author: ' + commit_dict['commit_author'] +
                      ', Commit date: ' + commit_dict['commit_created_date'])
    return result
