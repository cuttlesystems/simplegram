from pathlib import Path
from datetime import datetime
import json

from git import Repo

from common_utils.get_root_dir import get_project_root_dir


def create_file_with_info_about_last_commit() -> None:
    """
    Создает файл с информацией о коммите в корне проекта
    """
    repo = Repo(get_project_root_dir())
    latest_commit = repo.head.commit

    hash = str(latest_commit)[:7]
    author = str(latest_commit.author)
    created_date = str(datetime.fromtimestamp(latest_commit.committed_date))
    commit_dict = dict(commit_hash=hash, commit_author=author, commit_created_date=created_date)

    filename = str(get_project_root_dir() / 'current_commit_info.json')
    with open(filename, 'w') as file:
        json.dump(
            obj=commit_dict,
            fp=file,
            indent=4)


def read_info_from_file_about_commit() -> str:
    """
    Возвращает данные о текущем коммите, если файл с информацией существует.

    Returns:
        str: Данные о коммите.
    """
    result = 'Information about commit not found.'
    filename = str(get_project_root_dir() / 'mini_app' / 'current_commit_info.json')
    if Path(filename).exists():
        with open(filename, 'r') as commit_info:
            commit_dict = json.load(commit_info)
            if 'commit_hash' in commit_dict:
                result = ('Commit hash: ' + commit_dict['commit_hash'] +
                          ', Author: ' + commit_dict['commit_author'] +
                          ', Commit date: ' + commit_dict['commit_created_date'])
    else:
        print('------------->File with commit info not found.')
    return result
