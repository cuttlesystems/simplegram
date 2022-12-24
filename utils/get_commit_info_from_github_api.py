import os
import json
from datetime import datetime
from pytz import timezone

import requests
from dotenv import load_dotenv

load_dotenv()


def get_commit_info_from_github_api():
    """Временная колхоз версия"""
    result = 'Information about commit didn\'t found.'
    url = 'https://api.github.com/repos/cuttlesystems/tg_bot_constructor/commits'
    headers = {
        'Authorization': os.getenv('GITHUB_TOKEN'),
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
        except KeyError as error:
            print(f'Commit doesn\'t have field: {error}')
            result = 'Error occurred while getting commit info'
    return result
