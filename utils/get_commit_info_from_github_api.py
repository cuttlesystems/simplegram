import sys
import json
from pathlib import Path
from datetime import datetime
from pytz import timezone

import requests

from utils.get_root_dir import get_project_root_dir


def get_commit_info_from_github_api() -> dict:
    """Временная колхоз версия"""
    result = dict(error='Information about commit not found.')
    url = 'https://api.github.com/repos/cuttlesystems/tg_bot_constructor/commits'
    print(sys.argv[1])
    try:
        token = sys.argv[1]
    except IndexError:
        token = None
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
            result = f'Commit: {sha}, Author: {author}, Date: {date}'
            result = dict(commit_hash=sha, commit_author=author, commit_created_date=date)
        except KeyError as error:
            print(f'Commit doesn\'t have field: {error}')
            result = dict(error='Error occurred while getting commit info')
    return result


def create_json_file_with_commit_data(directory: Path, commit_data: dict) -> None:
    filename = str(directory / 'current_commit_info.json')
    with open(filename, 'w') as file:
        json.dump(
            obj=commit_data,
            fp=file,
            indent=4)


if __name__ == '__main__':
    commit_data_dict = get_commit_info_from_github_api()
    create_json_file_with_commit_data(directory=get_project_root_dir(), commit_data=commit_data_dict)
