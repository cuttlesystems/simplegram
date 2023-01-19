from pathlib import Path
import json

from common_utils.get_root_dir import get_project_root_dir


def read_info_from_file_about_commit() -> str:
    """
    Возвращает данные о текущем коммите, если файл с информацией существует.

    Returns:
        str: Данные о коммите.
    """
    result = 'Information about commit not found.'
    filename = str(get_project_root_dir() / 'current_commit_info.json')
    if Path(filename).exists():
        with open(filename, 'r') as commit_info:
            commit_dict = json.load(commit_info)
            try:
                result = ('Commit hash: ' + commit_dict['commit_hash'] +
                          ', Author: ' + commit_dict['commit_author'] +
                          ', Commit date: ' + commit_dict['commit_created_date'])
            except KeyError:
                pass
    return result
