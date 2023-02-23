from datetime import datetime
import json

from git import Repo
from git.repo.base import InvalidGitRepositoryError

from scripts.deploy_server_utils import get_project_root_dir, get_commit_info_file_path


def create_file_with_info_about_last_commit() -> None:
    """
    define function to create file with information on last commit in repo - 'current_commit_info.json'
    :return:
        файл с информацией о коммите в корне проекта 'tg_bot_constructor'

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

    filename = get_commit_info_file_path()
    with open(filename, 'w') as file:
        json.dump(
            obj=commit_dict,
            fp=file,
            indent=4)
