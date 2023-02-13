"""
модуль с дополнительными функциями, которые используются при разворачивании backend'а приложения на сервере
"""
import os
from pathlib import Path

from dataclasses import dataclass

import json

from subprocess import run

import docker


@dataclass(slots=True)
class DockerRegistryCredentials:
    docker_registry_server_url: str
    username: str
    password: str


@dataclass(slots=True)
class BackendServerCredentials:
    backend_server_ip: str
    username: str
    password: str


def write_dockerregistrycredentials() -> None:
    """
    write docker registry credentials into 'dockerregistrycredentials.json' file
    Returns: 'dockerregistrycredentials.json' file with credentials to login into
                private docker registry

    """
    docker_registry_credentials = DockerRegistryCredentials(
        docker_registry_server_url=input(
            '\nEnter docker registry server url (push \'Enter\' for default - "https://ramasuchka.kz:4443"): '
        ),
        username=input(
            'Enter username to login into docker registry: '
        ),
        password=input(
            'Enter password to login into docker: '
        )
    )
    if docker_registry_credentials.docker_registry_server_url == '':
        docker_registry_credentials.docker_registry_server_url = 'https://ramasuchka.kz:4443'
    assert isinstance(docker_registry_credentials, DockerRegistryCredentials)
    params = {
        'docker_registry_server_url': docker_registry_credentials.docker_registry_server_url,
        'username': docker_registry_credentials.username,
        'password': docker_registry_credentials.password
    }
    with open('dockerregistrycredentials.json', 'wt') as conffile:
        json.dump(params, conffile)
    print(
        f'\n--- Credentials to login into private docker registry were written into \'dockerregistrycredentials.json\','
        f' content: \n      {params} ---'
    )


def read_dockerregistrycredentials() -> DockerRegistryCredentials:
    """
    read docker registry credentials from 'dockerregistrycredentials.json' file
    Returns: read credentials to login into private docker registry from
                'dockerregistrycredentials.json' file if this file exists or
                outputs the message that one should create file with credentials if
                there is no 'dockerregistrycredentials.json' file

    """
    with open('dockerregistrycredentials.json', 'rt', encoding='utf-8') as conffile:
        docker_registry_credentials = json.load(conffile)
        # docker_registry_server_url = docker_registry_credentials['docker_registry_server_url']
        # username = docker_registry_credentials['username']
        # password = docker_registry_credentials['password']

        docker_registry_credentials = DockerRegistryCredentials(
            docker_registry_server_url=docker_registry_credentials['docker_registry_server_url'],
            username=docker_registry_credentials['username'],
            password=docker_registry_credentials['password'],
        )
        print(f'\nconffile: {conffile}')
        # print(f'\nconffile content - \'docker_registry_credentials\' instance:\n'
        #       f'{docker_registry_credentials}')
        # print(f'\ndockerregistrycredentials_content: {docker_registry_credentials}')
        # print(f'\nCredentials to login')
        # print(f'private docker registry server url: {docker_registry_credentials.docker_registry_server_url}')
        # print(f'username: {docker_registry_credentials.username}')
        # print(f'password: {docker_registry_credentials.password}')

        return docker_registry_credentials


# if __name__ == '__main__':
#     docker_registry_credentials_json_file_name = 'dockerregistrycredentials.json'
#     # путь для проверки существования файла 'dockerregistrycredentials.json' (с данными для входа в docker registry)
#     #  в директории "..\deploy\deploy_server\scripts"
#     search_dir_path = Path(__file__).parent
#     docker_registry_credentials_json_file_path = Path(search_dir_path) / docker_registry_credentials_json_file_name
#
#     print(f'\n\'dockerregistrycredentials.json\' file search path: {search_dir_path}')
#     # print(f'Current file name: {search_dir_path.name}')
#     print(f'\'dockerregistrycredentials.json\' file path: {docker_registry_credentials_json_file_path}')
#     if os.path.exists(docker_registry_credentials_json_file_path):
#         docker_registry_credentials = read_dockerregistrycredentials()
#     else:
#         write_dockerregistrycredentials()
#         docker_registry_credentials = read_dockerregistrycredentials()

def get_docker_registry_credentials() -> DockerRegistryCredentials:
    """

    :return:
    """
    docker_registry_credentials_json_file_name = 'dockerregistrycredentials.json'
    # путь для проверки существования файла 'dockerregistrycredentials.json' (с данными для входа в docker registry)
    #  в директории "..\deploy\deploy_server\scripts"
    search_dir_path = Path(__file__).parent
    docker_registry_credentials_json_file_path = Path(search_dir_path) / docker_registry_credentials_json_file_name

    print(f'\n\'dockerregistrycredentials.json\' file search path: {search_dir_path}')
    # print(f'Current file name: {search_dir_path.name}')
    print(f'\'dockerregistrycredentials.json\' file path: {docker_registry_credentials_json_file_path}')
    if os.path.exists(docker_registry_credentials_json_file_path):
        docker_registry_credentials = read_dockerregistrycredentials()
        print(f'\n\'dockerregistrycredentials.json\' file already exists in search path')
        # print(f'\nCredentials to login')
        # print(f'private docker registry server url: {docker_registry_credentials.docker_registry_server_url}')
        # print(f'username: {docker_registry_credentials.username}')
        # print(f'password: {docker_registry_credentials.password}')
    else:
        write_dockerregistrycredentials()
        docker_registry_credentials = read_dockerregistrycredentials()
        print(f'\n\'dockerregistrycredentials.json\' file saved')
        print(f'\nCredentials to login')
        print(f'private docker registry server url: {docker_registry_credentials.docker_registry_server_url}')
        print(f'username: {docker_registry_credentials.username}')
        print(f'password: {docker_registry_credentials.password}')
    return docker_registry_credentials


def write_backend_server_credentials() -> None:
    """
    write application backend server credentials into 'backendservercredentials.json' file
    Returns: 'backendservercredentials.json' file with credentials to establish SSH connection
                with remote server where the application backend is deployed

    """
    backend_server_credentials = BackendServerCredentials(
        backend_server_ip=input(
            '\nEnter backend server ip (push \'Enter\' for default - \"185.146.3.196 ramashechka.kz\"): '
        ),
        username=input(
            'Enter username to login into remote server (push \'Enter\' for default - \"ubuntu\"): '
        ),
        password=input(
            'Enter password to login into remote server (push \'Enter\' for default - \"bZ@gfkgou2qg\"): '
        )
    )
    if backend_server_credentials.backend_server_ip == '':
        backend_server_credentials.backend_server_ip = '185.146.3.196'
    if backend_server_credentials.username == '':
        backend_server_credentials.username = 'ubuntu'
    if backend_server_credentials.password == '':
        backend_server_credentials.password = 'bZ@gfkgou2qg'
    assert isinstance(backend_server_credentials, BackendServerCredentials)
    params = {
        'backend_server_ip': backend_server_credentials.backend_server_ip,
        'username': backend_server_credentials.username,
        'password': backend_server_credentials.password
    }
    with open('backendservercredentials.json', 'wt') as conffile:
        json.dump(params, conffile)
    print(
        f'\n--- Credentials to establish SSH connection were written into \'backendservercredentials.json\','
        f' content: \n      {params} ---'
    )


def read_backend_server_credentials() -> BackendServerCredentials:
    """
    read application backend server credentials from 'backendservercredentials.json' file
    Returns: read credentials to establish SSH connection with remote server where the application backend is deployed
                from 'backendservercredentials.json' file if this file exists or
                outputs the message that one should create file with credentials if
                there is no 'backendservercredentials.json' file

    """
    with open('backendservercredentials.json', 'rt', encoding='utf-8') as conffile:
        backend_server_credentials = json.load(conffile)
        # backend_server_ip = backend_server_credentials['backend_server_ip']
        # username = backend_server_credentials['username']
        # password = backend_server_credentials['password']

        backend_server_credentials = BackendServerCredentials(
            backend_server_ip=backend_server_credentials['backend_server_ip'],
            username=backend_server_credentials['username'],
            password=backend_server_credentials['password'],
        )
        print(f'\nconffile: {conffile}')
        # print(f'\nconffile content - \'backend_server_credentials\' instance:\n'
        #       f'{backend_server_credentials}')
        # print(f'\nbackendservercredentials_content: {backend_server_credentials}')
        # print(f'\nCredentials to establish SSH connection with remote server')
        # print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
        # print(f'username: {backend_server_credentials.username}')
        # print(f'password: {backend_server_credentials.password}')

        return backend_server_credentials


def get_backend_server_credentials() -> BackendServerCredentials:
    """

    :return:
    """
    backend_server_credentials_json_file_name = 'backendservercredentials.json'
    # путь для проверки существования файла 'backendservercredentials.json'
    #  (с данными для установления соединения по SSH с удалённым сервером)
    #  в директории "..\deploy\deploy_server\scripts"
    search_dir_path = Path(__file__).parent
    backend_server_credentials_json_file_path = Path(search_dir_path) / backend_server_credentials_json_file_name

    print(f'\n\'backendservercredentials.json\' file search path: {search_dir_path}')
    # print(f'Current file name: {search_dir_path.name}')
    print(f'\'backendservercredentials.json\' file path: {backend_server_credentials_json_file_path}')
    if os.path.exists(backend_server_credentials_json_file_path):
        backend_server_credentials = read_backend_server_credentials()
        print(f'\n\'backendservercredentials.json\' file already exists in search path')
        # print(f'\nCredentials to establish SSH connection with remote server')
        # print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
        # print(f'username: {backend_server_credentials.username}')
        # print(f'password: {backend_server_credentials.password}')
    else:
        write_backend_server_credentials()
        backend_server_credentials = read_backend_server_credentials()
        print(f'\n\'backendservercredentials.json\' file saved')
        print(f'\nCredentials to establish SSH connection with remote server')
        print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
        print(f'username: {backend_server_credentials.username}')
        print(f'password: {backend_server_credentials.password}')
    return backend_server_credentials


def docreg_login_locally():
    # get_docker_registry_credentials()
    # print(f'{get_docker_registry_credentials}')
    print(
        f'\nprivate docker registry logging in locally with credentials saved to'
        f'\'dockerregistrycredentials.json\' file to push docker image'
    )
    print(f'private docker registry server url: {get_docker_registry_credentials().docker_registry_server_url}')

    # run([f'docker', '-v'])
    run(
        [
            f'docker',
            'login',
            f'{get_docker_registry_credentials().docker_registry_server_url}',
            '--username', f'{get_docker_registry_credentials().username}',
            '--password', f'{get_docker_registry_credentials().password}'
        ]
    )


def docreg_logout_locally():
    """

    :return:
    """
    print(
        f'\nprivate docker registry logging out locally after docker image push'
    )
    run(
        [
            f'docker',
            'logout',
            f'{get_docker_registry_credentials().docker_registry_server_url}'
        ]
    )


    # private docker registry logging in remotely through 'ssh' and
    #  with 2 command line parameters (without '--password-stdin') to pull docker image to the server
    #  for 'simple_gram' application background image deployment
def docreg_login_remotely():
    """

    :return:
    """
    # ssh ubuntu@185.146.3.196 'bash -s '$(cat ~/scripts/docreg_password.txt)' '$(cat ~/scripts/docreg_password.txt)'' -- < ~/scripts/docreg_login.sh

    # Create a client connecting to Docker daemon via SSH
    client = docker.DockerClient(
        base_url=f'ssh://{get_backend_server_credentials().username}@{get_backend_server_credentials().backend_server_ip}',
        use_ssh_client=True
    )

    print(f'SSH connection to remote server established')
    print(f'application backend server ip: {get_backend_server_credentials().backend_server_ip}')
    print(f'username: {get_backend_server_credentials().username}')

    print(
        f'\nprivate docker registry logging in remotely with credentials saved to'
        f'\'dockerregistrycredentials.json\' file to pull docker image'
    )
    # print(f'private docker registry server url: {get_docker_registry_credentials.docker_registry_server_url}')
    client.login(username='admin', password='admin', registry='https://ramasuchka.kz:4443')
    print(
        f'\nSuccessfully logged in to private docker registry from the remote server - '
        f'{get_backend_server_credentials().backend_server_ip}'
    )
