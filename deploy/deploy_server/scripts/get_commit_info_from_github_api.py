import sys
import json
from pathlib import Path
from datetime import datetime
from pytz import timezone
import requests

from scripts.deploy_server_utils import get_script_dir_path


def get_commit_info_from_github_api(token_with_bearer: str) -> dict:
    """Временная колхоз версия"""
    result = dict(error='Information about commit not found')
    url = 'https://api.github.com/repos/cuttlesystems/tg_bot_constructor/commits'
    token = token_with_bearer
    headers = {
        'Authorization': token,
        'Accept': 'application/vnd.github+json'
    }
    branch_name = 'main'
    params = {
        'sha': branch_name
    }
    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == requests.status_codes.codes.ok:
        try:
            commit = json.loads(response.text)[0]
            sha = commit['sha'][:7]
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date'].replace('T', ' ').replace('Z', '')
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            default_tz = timezone('UTC')
            alma_tz = timezone('Asia/Almaty')
            date = date.replace(tzinfo=default_tz)
            date = date.astimezone(alma_tz)
            date = str(date).replace('+06:00', '')
            result = dict(commit_hash=sha, commit_author=author, commit_created_date=date)
        except KeyError as error:
            print(f'Commit doesn\'t have field: {error}')
            result = dict(error='Error occurred while getting commit info')
    else:
        print(f'is error ({response.status_code}): {response.text}')
    print(f'Get commit result: {result}')
    return result


def get_project_root_dir() -> Path:
    """
    define function to get 'tg_bot_constructor' project directory path
    :return:

    """
    project_root_dir = get_script_dir_path().parent.parent.parent
    return project_root_dir


def get_commit_info_file_path() -> Path:
    """

    :return:

    """
    commit_info_file_path = get_project_root_dir() / 'current_commit_info.json'
    return commit_info_file_path


def create_json_file_with_commit_data(commit_data: dict) -> None:
    commit_info_file_path = get_commit_info_file_path()
    with open(commit_info_file_path, 'w', encoding='utf-8') as commit_info_file:
        json.dump(
            obj=commit_data,
            fp=commit_info_file,
            indent=4)


# if __name__ == '__main__':
# commit_data_dict = get_commit_info_from_github_api(token_with_bearer)
# create_json_file_with_commit_data(directory=get_project_root_dir(), commit_data=commit_data_dict)
