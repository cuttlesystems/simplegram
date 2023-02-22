import json
from pathlib import Path

from common_utils.get_root_dir import get_project_root_dir


def read_info_from_file_about_commit() -> str:
    """
    Возвращает данные о текущем коммите, если файл с информацией существует

    Returns:
        str: Данные о коммите
    """
    result = 'Information about commit not found'
    # при deploy'е через bash-скрипт
    commit_info_through_bash_json_file_path = get_project_root_dir() / 'mini_app' / 'current_commit_info.json'
    # при deploy'е через python-скрипт
    commit_info_through_python_json_file_path = (
        get_project_root_dir().parent / 'deploy_folder' / 'tg_bot_constructor' / 'mini_app' / 'current_commit_info.json'
    )
    if Path(commit_info_through_bash_json_file_path).exists():
        filename = str(commit_info_through_bash_json_file_path)
        with open(filename, 'r') as commit_info:
            commit_dict = json.load(commit_info)
            if 'commit_hash' in commit_dict:
                result = ('Commit hash: ' + commit_dict['commit_hash'] +
                          ', Author: ' + commit_dict['commit_author'] +
                          ', Commit date: ' + commit_dict['commit_created_date'])
    elif Path(commit_info_through_python_json_file_path).exists():
        filename = str(commit_info_through_python_json_file_path)
        with open(filename, 'r') as commit_info:
            commit_dict = json.load(commit_info)
            if 'commit_hash' in commit_dict:
                result = ('Commit hash: ' + commit_dict['commit_hash'] +
                          ', Author: ' + commit_dict['commit_author'] +
                          ', Commit date: ' + commit_dict['commit_created_date'])
    else:
        print('-------------> File with commit info not found')
    return result
