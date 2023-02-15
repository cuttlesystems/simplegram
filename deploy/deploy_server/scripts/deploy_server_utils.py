"""
модуль с дополнительными функциями, которые используются при разворачивании backend'а приложения на сервере
"""
import os
from pathlib import Path

from dataclasses import dataclass

import json

from subprocess import run

import docker
# import paramiko


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


def get_docker_registry_credentials_json_file_path() -> Path:
    """

    :return:
    """
    docker_registry_credentials_json_file_name = 'dockerregistrycredentials.json'
    # путь для проверки существования файла 'backendservercredentials.json'
    #  (с данными для установления соединения по SSH с удалённым сервером)
    #  в директории "..\deploy\deploy_server\scripts"
    search_dir_path = Path(__file__).parent
    docker_registry_credentials_json_file_path = search_dir_path / docker_registry_credentials_json_file_name

    # print(f'\n\'backendservercredentials.json\' file search path: {search_dir_path}')
    # # print(f'Current file name: {search_dir_path.name}')
    # print(f'\'backendservercredentials.json\' file path: {backend_server_credentials_json_file_path}')
    return docker_registry_credentials_json_file_path


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
    with open(get_docker_registry_credentials_json_file_path(), 'wt', encoding='utf-8') as conffile:
        json.dump(params, conffile)
    # print(
    #     f'\n--- Credentials to login into private docker registry were written into \'dockerregistrycredentials.json\','
    #     f' content: \n      {params} ---'
    # )
    print(
        f'\n---------------------------------------------------------\n'
        f'Credentials to login into private docker registry were written into '
        f'\'{get_docker_registry_credentials_json_file_path()}\',\n'
        f'content: {params}'
        f'\n---------------------------------------------------------\n'
    )


def read_dockerregistrycredentials() -> DockerRegistryCredentials:
    """
    read docker registry credentials from 'dockerregistrycredentials.json' file
    Returns: read credentials to login into private docker registry from
                'dockerregistrycredentials.json' file if this file exists or
                outputs the message that one should create file with credentials if
                there is no 'dockerregistrycredentials.json' file

    """
    with open(get_docker_registry_credentials_json_file_path(), 'rt', encoding='utf-8') as conffile:
        docker_registry_credentials = json.load(conffile)
        # docker_registry_server_url = docker_registry_credentials['docker_registry_server_url']
        # username = docker_registry_credentials['username']
        # password = docker_registry_credentials['password']

        docker_registry_credentials = DockerRegistryCredentials(
            docker_registry_server_url=docker_registry_credentials['docker_registry_server_url'],
            username=docker_registry_credentials['username'],
            password=docker_registry_credentials['password'],
        )
        # print(f'\nconffile: {conffile}')
        # print(f'\nconffile content - \'docker_registry_credentials\' instance:\n'
        #       f'{docker_registry_credentials}')
        # print(f'\ndockerregistrycredentials_content: {docker_registry_credentials}')
        # print(f'\nCredentials to login')
        # print(f'private docker registry server url: {docker_registry_credentials.docker_registry_server_url}')
        # print(f'username: {docker_registry_credentials.username}')
        # print(f'password: {docker_registry_credentials.password}')

    return docker_registry_credentials


def get_docker_registry_credentials() -> DockerRegistryCredentials:
    """

    :return:
    """
    # docker_registry_credentials_json_file_name = 'dockerregistrycredentials.json'
    # # путь для проверки существования файла 'dockerregistrycredentials.json' (с данными для входа в docker registry)
    # #  в директории "..\deploy\deploy_server\scripts"
    # search_dir_path = Path(__file__).parent
    # docker_registry_credentials_json_file_path = Path(search_dir_path) / docker_registry_credentials_json_file_name
    #
    # print(f'\n\'dockerregistrycredentials.json\' file search path: {search_dir_path}')
    # # print(f'Current file name: {search_dir_path.name}')
    # print(f'\'dockerregistrycredentials.json\' file path: {docker_registry_credentials_json_file_path}')
    if os.path.exists(get_docker_registry_credentials_json_file_path()):
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


def get_backend_server_credentials_json_file_path() -> Path:
    """

    :return:
    """
    backend_server_credentials_json_file_name = 'backendservercredentials.json'
    # путь для проверки существования файла 'backendservercredentials.json'
    #  (с данными для установления соединения по SSH с удалённым сервером)
    #  в директории "..\deploy\deploy_server\scripts"
    search_dir_path = Path(__file__).parent
    backend_server_credentials_json_file_path = search_dir_path / backend_server_credentials_json_file_name

    # print(f'\n\'backendservercredentials.json\' file search path: {search_dir_path}')
    # # print(f'Current file name: {search_dir_path.name}')
    # print(f'\'backendservercredentials.json\' file path: {backend_server_credentials_json_file_path}')
    return backend_server_credentials_json_file_path


def write_backend_server_credentials() -> None:
    """
    write application backend server credentials into 'backendservercredentials.json' file
    Returns: 'backendservercredentials.json' file with credentials to establish SSH connection
                with remote server where the application backend is deployed

    """
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<----------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
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
    with open(get_backend_server_credentials_json_file_path(), 'wt', encoding='utf-8') as conffile:
        json.dump(params, conffile)
    print(
        f'\n---------------------------------------------------------\n'
        f'Credentials to establish SSH connection were written into '
        f'\'{get_backend_server_credentials_json_file_path()}\',\n'
        f'content: {params}'
        f'\n---------------------------------------------------------\n'
    )


def read_backend_server_credentials() -> BackendServerCredentials:
    """
    read application backend server credentials from 'backendservercredentials.json' file
    Returns: read credentials to establish SSH connection with remote server where the application backend is deployed
                from 'backendservercredentials.json' file if this file exists or
                outputs the message that one should create file with credentials if
                there is no 'backendservercredentials.json' file

    """
    with open(get_backend_server_credentials_json_file_path(), 'rt', encoding='utf-8') as conffile:
        backend_server_credentials = json.load(conffile)
    # backend_server_ip = backend_server_credentials['backend_server_ip']
    # username = backend_server_credentials['username']
    # password = backend_server_credentials['password']

    backend_server_credentials = BackendServerCredentials(
        backend_server_ip=backend_server_credentials['backend_server_ip'],
        username=backend_server_credentials['username'],
        password=backend_server_credentials['password'],
    )
    # print(f'\nconffile: {conffile}')
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
    # backend_server_credentials_json_file_name = 'backendservercredentials.json'
    # # путь для проверки существования файла 'backendservercredentials.json'
    # #  (с данными для установления соединения по SSH с удалённым сервером)
    # #  в директории "..\deploy\deploy_server\scripts"
    # search_dir_path = Path(__file__).parent
    # backend_server_credentials_json_file_path = Path(search_dir_path) / backend_server_credentials_json_file_name
    #
    # print(f'\n\'backendservercredentials.json\' file search path: {search_dir_path}')
    # # print(f'Current file name: {search_dir_path.name}')
    # print(f'\'backendservercredentials.json\' file path: {backend_server_credentials_json_file_path}')
    if os.path.exists(get_backend_server_credentials_json_file_path()):
        backend_server_credentials = read_backend_server_credentials()
        print(
                f'\n\'backendservercredentials.json\' file already exists in search path:\n'
                f'{get_backend_server_credentials_json_file_path().parent}'
        )
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


def docreg_login_locally(docker_registry_credentials: DockerRegistryCredentials):
    # get_docker_registry_credentials()
    # print(f'{get_docker_registry_credentials}')
    print(
        f'\n--- private docker registry logging in locally with credentials saved to'
        f'\'dockerregistrycredentials.json\' file to push docker image ---'
    )
    print(f'\nprivate docker registry server url: {docker_registry_credentials.docker_registry_server_url}')

    # run([f'docker', '-v'])
    run(
        [
            f'docker',
            'login',
            f'{docker_registry_credentials.docker_registry_server_url}',
            '--username', f'{docker_registry_credentials.username}',
            '--password', f'{docker_registry_credentials.password}'
        ]
    )


def docreg_logout_locally(docker_registry_credentials: DockerRegistryCredentials):
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
            f'{docker_registry_credentials.docker_registry_server_url}'
        ]
    )


# private docker registry logging in remotely through 'ssh' and
#  with 2 command line parameters (without '--password-stdin') to pull docker image to the server
#  for 'simple_gram' application background image deployment
def docreg_login_remotely(backend_server_credentials: BackendServerCredentials):
    """

    :return:
    """
    # ssh ubuntu@185.146.3.196 'bash -s '$(cat ~/scripts/docreg_password.txt)' '$(cat ~/scripts/docreg_password.txt)'' -- < ~/scripts/docreg_login.sh
    print('Check')

    # # Load SSH host keys.
    # ssh_client.load_system_host_keys()

    # Create a client connecting to Docker daemon via SSH
    docker_client = docker.DockerClient(
        base_url=f'ssh://{backend_server_credentials.username}@{backend_server_credentials.backend_server_ip}',
        use_ssh_client=True
    )

    print(f'SSH connection to remote server established')
    # print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
    # print(f'username: {backend_server_credentials.username}')

    print(
        f'\nprivate docker registry logging in remotely with credentials saved to'
        f'\'dockerregistrycredentials.json\' file to pull docker image'
    )
    # print(f'private docker registry server url: {docker_registry_credentials.docker_registry_server_url}')
    docker_client.login(username='admin', password='admin', registry='https://ramasuchka.kz:4443')
    print(
        f'\nSuccessfully logged in to private docker registry from the remote server - '
        # f'{backend_server_credentials.backend_server_ip}'
    )


def get_rsa_pub_key_directory_path() -> Path:
    """
    define function to get an RSA key directory path - '<user_path>/.ssh'
    :return:
    """
    # path to user directory
    user_path = Path('~').expanduser()
    print(f'Path to user directory: {user_path}')

    # path to '<user_path>/.ssh' directory
    rsa_pub_key_directory_path = user_path / '.ssh'
    print(f'Path to \'<user_path>/.ssh\' directory: {rsa_pub_key_directory_path}')
    return rsa_pub_key_directory_path


def get_rsa_pub_key_path() -> Path:
    """
    define function to get an RSA key path - '<user_path>/.ssh/id_rsa'
    :return:

    """
    # path to RSA key - '<user_path>/.ssh/id_rsa'
    rsa_pub_key_path = get_rsa_pub_key_directory_path() / 'id_rsa'
    print(f'Path to \'<user_path>/.ssh/id_rsa\' file: {rsa_pub_key_path}')
    return rsa_pub_key_path


def rsa_pub_key_is_present() -> bool:
    """
    define function to check if there is an RSA pub key already present in '<user_path>/.ssh' directory
    :return: bool
                'True' if RSA pub key is already present in '<user_path>/.ssh' directory
                'False' if there's no RSA pub key '<user_path>/.ssh' directory
    """
    if 'id_rsa.pub' in os.listdir(get_rsa_pub_key_directory_path()):
        return True
    else:
        return False


def show(msg):
    """
    define function to print debug messages and script process notifications
    :param msg: str
    :return: local print( ) function

    """
    print(msg)


def gen_ssh_key_pair() -> None:
    """
    define function to generate SSH key pair if it doesn't exist
    :return: SSH key pair
    """
    os.chdir(get_rsa_pub_key_directory_path())
    if rsa_pub_key_is_present():
        show(f'SSH pub key is already present in \'{get_rsa_pub_key_directory_path()}\' directory')
    else:
        # generate SSH key pair
        # subprocess.call('ssh-keygen', shell=True)
        # ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa <<< y
        run(
            [
                'ssh-keygen',
                '-q',
                '-t',
                'rsa',
                '-N',
                '',
                '-f',
                f'{get_rsa_pub_key_path()}'
                # '<<<',
                # 'y'
            ]
        )
        # command = "ssh-copy-id -p %s %s@%s" % (22, 'ubuntu', f'{get_backend_server_credentials().backend_server_ip}')
        # subprocess.call(command, shell=True)


def rsa_key_based_connect():
    import paramiko
    ssh_client = paramiko.SSHClient()

    # Load SSH host keys.
    ssh_client.load_system_host_keys()

    # transport = ssh_client.get_transport()
    host = f'{get_backend_server_credentials().backend_server_ip}'
    special_account = f'{get_backend_server_credentials().username}'
    # password = f'{get_backend_server_credentials().password}'
    private_key = paramiko.RSAKey.from_private_key_file(f'{get_rsa_pub_key_path()}')

    # client = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh_client.set_missing_host_key_policy(policy)

    # ssh_client.connect(host, disabled_algorithms={'keys': ['rsa-sha2-256', 'rsa-sha2-512']}, username=special_account, pkey=private_key, look_for_keys=False)
    # ssh_client.connect(host, username=special_account, password=password, pkey=private_key)
    ssh_client.connect(host, username=special_account, pkey=private_key)
    print(f'\nSSH connection established: {ssh_client}')
    return ssh_client


