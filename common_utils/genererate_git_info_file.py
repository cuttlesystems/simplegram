from pathlib import Path
from datetime import datetime
import json

from git import Repo
from git.repo.base import InvalidGitRepositoryError

from common_utils.get_root_dir import get_project_root_dir


def create_file_with_info_about_last_commit() -> None:
    """
    Создает файл с информацией о коммите в корне проекта
    """
    try:
        repo = Repo(get_project_root_dir())
    except InvalidGitRepositoryError:
        print(f'File .git not found in directory {get_project_root_dir()}')
        return
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
