"""
модуль с дополнительными функциями, которые используются при разворачивании backend'а приложения на сервере
"""
import os
import sys
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


@dataclass(slots=True)
class PostgresEnvVariables:
    DB_ENGINE: str
    DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DOMAIN_HOST: str
    HOST_PROTOCOL: str
    # 'DB_ENGINE=django.db.backends.postgresql
    # DB_NAME=bot_constructor
    # POSTGRES_USER=postgres
    # POSTGRES_PASSWORD=zarFad-huqdit-qavry0
    # DB_HOST=172.21.0.1
    # DB_PORT=5432
    # DOMAIN_HOST=ramasuchka.kz
    # HOST_PROTOCOL=https'


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
        # print(
        #         f'\n\'backendservercredentials.json\' file already exists in search path:\n'
        #         f'{get_backend_server_credentials_json_file_path().parent}'
        # )
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


def docker_create_image_locally():
    # Create a client connecting to Docker daemon locally
    docker_client_local = docker.from_env()
    # Create a client connecting to Docker daemon via SSH
    # docker_client = docker.DockerClient(
    #     base_url=f'ssh://{backend_server_credentials.username}@{backend_server_credentials.backend_server_ip}',
    #     use_ssh_client=True
    # )
    print(
        f'\nprivate docker registry logging in locally with credentials saved to'
        f'\'dockerregistrycredentials.json\' file to create and push docker image'
    )

    docker_client_local.login(username='admin', password='admin', registry='https://ramasuchka.kz:4443')
    print(
        f'\n--------------------------------------------------------------------------------------------------------\n'
        f'\nSuccessfully logged in to private docker registry from the local machine with local Docker daemon '
        # f'{backend_server_credentials.backend_server_ip}'
        f'\n--------------------------------------------------------------------------------------------------------\n'
    )


# private docker registry logging in remotely through 'ssh' and
#  with 2 command line parameters (without '--password-stdin') to pull docker image to the server
#  for 'simple_gram' application background image deployment
def docreg_login_remotely(backend_server_credentials: BackendServerCredentials):
    """

    :return:
    """
    # ssh ubuntu@185.146.3.196 'bash -s '$(cat ~/scripts/docreg_password.txt)' '$(cat ~/scripts/docreg_password.txt)'' -- < ~/scripts/docreg_login.sh
    # print('\nCheck')

    # # Load SSH host keys.
    # ssh_client.load_system_host_keys()

    # Create a client connecting to Docker daemon via SSH
    docker_client = docker.DockerClient(
        base_url=f'ssh://{backend_server_credentials.username}@{backend_server_credentials.backend_server_ip}',
        use_ssh_client=True
    )

    # print(f'\nSSH connection to remote server established')
    # print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
    # print(f'username: {backend_server_credentials.username}')

    print(
        f'\nprivate docker registry logging in remotely with credentials saved to'
        f'\'dockerregistrycredentials.json\' file to pull docker image'
    )

    docker_client.login(username='admin', password='admin', registry='https://ramasuchka.kz:4443')
    print(
        f'\n--------------------------------------------------------------------------------------------------------\n'
        f'\nSuccessfully logged in to private docker registry on the remote server - '
        f'{backend_server_credentials.backend_server_ip}'
        f'\n--------------------------------------------------------------------------------------------------------\n'
    )


def get_rsa_pub_key_directory_path() -> Path:
    """
    define function to get an RSA key directory path - '<user_path>/.ssh'
    :return:
    """
    # path to user directory
    user_path = Path('~').expanduser()
    # print(f'Path to user directory: {user_path}')

    # path to '<user_path>/.ssh' directory
    rsa_pub_key_directory_path = user_path / '.ssh'
    # print(f'Path to \'<user_path>/.ssh\' directory: {rsa_pub_key_directory_path}')
    return rsa_pub_key_directory_path


def get_rsa_key_path() -> Path:
    """
    define function to get an RSA key path - '<user_path>/.ssh/id_rsa'
    :return:

    """
    # path to RSA key - '<user_path>/.ssh/id_rsa'
    rsa_private_key_path = get_rsa_pub_key_directory_path() / 'id_rsa'
    # print(f'Path to \'<user_path>/.ssh\' directory: {rsa_private_key_path.parent}')
    # print(f'Path to \'<user_path>/.ssh/id_rsa\' file: {rsa_private_key_path}')
    return rsa_private_key_path


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
        show(f'\nSSH pub key is already present in \'{get_rsa_pub_key_directory_path()}\' directory')
        # print(f'Path to \'<user_path>/.ssh\' directory: {rsa_private_key_path.parent}')
        # print(f'Path to \'<user_path>/.ssh/id_rsa\' file: {rsa_private_key_path}')
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
                f'{get_rsa_key_path()}'
                # '<<<',
                # 'y'
            ]
        )
        # command = "ssh-copy-id -p %s %s@%s" % (22, 'ubuntu', f'{get_backend_server_credentials().backend_server_ip}')
        # subprocess.call(command, shell=True)


def rsa_key_based_connect():
    """

    :return:
    """
    import paramiko
    ssh_client = paramiko.SSHClient()

    # Load SSH host keys.
    ssh_client.load_system_host_keys()

    # transport = ssh_client.get_transport()
    host = f'{get_backend_server_credentials().backend_server_ip}'
    special_account = f'{get_backend_server_credentials().username}'
    password = f'{get_backend_server_credentials().password}'
    private_key = paramiko.RSAKey.from_private_key_file(f'{get_rsa_key_path()}')

    # client = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh_client.set_missing_host_key_policy(policy)

    # ssh_client.connect(host, disabled_algorithms={'keys': ['rsa-sha2-256', 'rsa-sha2-512']}, username=special_account, pkey=private_key, look_for_keys=False)
    # ssh_client.connect(host, username=special_account, password=password, pkey=private_key)
    # ssh_client.connect(host, username=special_account, pkey=private_key, look_for_keys=True)
    ssh_client.connect(host, username=special_account, password=password)
    print(f'\nSSH connection to remote server established: {ssh_client}')
    return ssh_client


def move_rsa_pub_key_to_remote() -> None:
    """

    :return:
    """
    rsa_pub_key_path = get_rsa_key_path().with_suffix('.pub')
    print(f'Path to public rsa key \'<user_path>/.ssh/id_rsa.pub\' file: {rsa_pub_key_path}')
    with open(f'{rsa_pub_key_path}', 'rt', encoding='utf-8') as rsa_pub_key_content_file:
        rsa_pub_key_content = rsa_pub_key_content_file.read()
        # backend_server_ip = backend_server_credentials['backend_server_ip']
        # username = backend_server_credentials['username']
        # password = backend_server_credentials['password']

        # backend_server_credentials = BackendServerCredentials(
        #     backend_server_ip=backend_server_credentials['backend_server_ip'],
        #     username=backend_server_credentials['username'],
        #     password=backend_server_credentials['password'],
        # )
        print(f'\nrsa_pub_key_content file: {rsa_pub_key_content_file}')
        print(f'\nrsa_pub_key_content:\n'
              f'{rsa_pub_key_content}')
        # print(f'\nconffile content - \'backend_server_credentials\' instance:\n'
        #       f'{backend_server_credentials}')
        # print(f'\nbackendservercredentials_content: {backend_server_credentials}')
        # print(f'\nCredentials to establish SSH connection with remote server')
        # print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
        # print(f'username: {backend_server_credentials.username}')
        # print(f'password: {backend_server_credentials.password}')

        # return backend_server_credentials
    # работает строка ниже
    # command = f'sudo echo "{backend_server_credentials}" >> ~/.ssh/authorized_keys'
    # command = str('sudo echo b >> ~/test.txt')
    # command = 'echo {backend_server_credentials} >> ~/.ssh/authorized_keys'.format(backend_server_credentials=backend_server_credentials)
    ssh_stdin, ssh_stdout, ssh_stderr = rsa_key_based_connect().exec_command(
        f'echo "{rsa_pub_key_content}" >> ~/.ssh/authorized_keys'
    )
    ssh_stdin.close()


def get_postgres_env_file_path() -> Path:
    """
    define function to get '.env' file (with postgres environment variables) path
    :return:
        '.env' file path
    """
    postgres_env_file_name = '.env'
    # путь для проверки существования файла '.env'
    #  (с переменными оружения для функционирования базы данных postgres)
    #  в директории "..\deploy\deploy_server\infra"
    search_dir_path = Path(__file__).parent.parent / 'infra'
    postgres_env_file_path = search_dir_path / postgres_env_file_name

    print(f'\n\'.env\' file search path: {search_dir_path}')
    print(f'Current file name: {search_dir_path.name}')
    print(f'\'.env\' file path: {postgres_env_file_path}')
    return postgres_env_file_path


def write_postgres_env_variables_json() -> None:
    """
    write postgres environment variables into '.env' file
    Returns:
        '.env' file with postgres environment variables for postgresDB functionality

    """
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<----------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    postgres_env_variables = PostgresEnvVariables(
        DB_ENGINE=input(
            '\nEnter \'DB_ENGINE\' value (push \'Enter\' for default - \"django.db.backends.postgresql\"): '
        ),
        DB_NAME=input(
            'Enter \'DB_NAME\' value (push \'Enter\' for default - \"bot_constructor\"): '
        ),
        POSTGRES_USER=input(
            'Enter \'POSTGRES_USER\' value (push \'Enter\' for default - \"postgres\"): '
        ),
        POSTGRES_PASSWORD=input(
            'Enter \'POSTGRES_PASSWORD\' value (push \'Enter\' for default - \"zarFad-huqdit-qavry0\"): '
        ),
        DB_HOST=input(
            'Enter \'DB_HOST\' value (push \'Enter\' for default - \"172.21.0.1\"): '
        ),
        DB_PORT=input(
            'Enter \'DB_PORT\' value (push \'Enter\' for default - \"5432\"): '
        ),
        DOMAIN_HOST=input(
            'Enter \'DOMAIN_HOST\' value (push \'Enter\' for default - \"ramasuchka.kz\"): '
        ),
        HOST_PROTOCOL=input(
            'Enter \'HOST_PROTOCOL\' value (push \'Enter\' for default - \"https\"): '
        )
    )
    if postgres_env_variables.DB_ENGINE == '':
        postgres_env_variables.DB_ENGINE = 'django.db.backends.postgresql'
    if postgres_env_variables.DB_NAME == '':
        postgres_env_variables.DB_NAME = 'bot_constructor'
    if postgres_env_variables.POSTGRES_USER == '':
        postgres_env_variables.POSTGRES_USER = 'postgres'
    if postgres_env_variables.POSTGRES_PASSWORD == '':
        postgres_env_variables.POSTGRES_PASSWORD = 'zarFad-huqdit-qavry0'
    if postgres_env_variables.DB_HOST == '':
        postgres_env_variables.DB_HOST = '172.21.0.1'
    if postgres_env_variables.DB_PORT == '':
        postgres_env_variables.DB_PORT = '5432'
    if postgres_env_variables.DOMAIN_HOST == '':
        postgres_env_variables.DOMAIN_HOST = 'ramasuchka.kz'
    if postgres_env_variables.HOST_PROTOCOL == '':
        postgres_env_variables.HOST_PROTOCOL = 'https'
    assert isinstance(postgres_env_variables, PostgresEnvVariables)
    params = {
        'DB_ENGINE': postgres_env_variables.DB_ENGINE,
        'DB_NAME': postgres_env_variables.DB_NAME,
        'POSTGRES_USER': postgres_env_variables.POSTGRES_USER,
        'POSTGRES_PASSWORD': postgres_env_variables.POSTGRES_PASSWORD,
        'DB_HOST': postgres_env_variables.DB_HOST,
        'DB_PORT': postgres_env_variables.DB_PORT,
        'DOMAIN_HOST': postgres_env_variables.DOMAIN_HOST,
        'HOST_PROTOCOL': postgres_env_variables.HOST_PROTOCOL
    }
    with open(f'{get_postgres_env_file_path()}_json', 'wt', encoding='utf-8') as envfile:
        json.dump(params, envfile)
    print(
        f'\n---------------------------------------------------------\n'
        f'postgres environment variables were written into '
        f'\'{get_postgres_env_file_path()}_json\',\n'
        f'content: {params}'
        f'\n---------------------------------------------------------\n'
    )


def convert_postgres_env_variables_json_to_text() -> None:
    """
    convert postgres environment variables from '.env.json' file into '.env' file
    Returns:
        '.env' file with postgres environment variables for postgresDB functionality

    """
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<----------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    postgres_env_variables = get_postgres_env_variables()
    assert isinstance(postgres_env_variables, PostgresEnvVariables)

    with open(get_postgres_env_file_path(), 'wt', encoding='utf-8') as envfile:
        envfile.writelines(f'DB_ENGINE={postgres_env_variables.DB_ENGINE}\n')
        envfile.writelines(f'DB_NAME={postgres_env_variables.DB_NAME}\n')
        envfile.writelines(f'POSTGRES_USER={postgres_env_variables.POSTGRES_USER}\n')
        envfile.writelines(f'POSTGRES_PASSWORD={postgres_env_variables.POSTGRES_PASSWORD}\n')
        envfile.writelines(f'DB_HOST={postgres_env_variables.DB_HOST}\n')
        envfile.writelines(f'DB_PORT={postgres_env_variables.DB_PORT}\n')
        envfile.writelines(f'DOMAIN_HOST={postgres_env_variables.DOMAIN_HOST}\n')
        envfile.writelines(f'HOST_PROTOCOL={postgres_env_variables.HOST_PROTOCOL}')
    print(
        f'\n---------------------------------------------------------\n'
        f'postgres environment variables were written into '
        f'\'{get_postgres_env_file_path()}\',\n'
        f'content:\n'
        f'DB_ENGINE={postgres_env_variables.DB_ENGINE}\n'
        f'DB_NAME={postgres_env_variables.DB_NAME}\n'
        f'POSTGRES_USER={postgres_env_variables.POSTGRES_USER}\n'
        f'POSTGRES_PASSWORD={postgres_env_variables.POSTGRES_PASSWORD}\n'
        f'DB_HOST={postgres_env_variables.DB_HOST}\n'
        f'DB_PORT={postgres_env_variables.DB_PORT}\n'
        f'DOMAIN_HOST={postgres_env_variables.DOMAIN_HOST}\n'
        f'HOST_PROTOCOL={postgres_env_variables.HOST_PROTOCOL}\n'
        f'\n---------------------------------------------------------\n'
    )


def read_postgres_env_variables_json() -> PostgresEnvVariables:
    """
    read postgres environment variables from '.env' file
    Returns:
        postgres environment variables' values from '.env' file needed for postgresDB functionality

    """
    with open(f'{get_postgres_env_file_path()}_json', 'rt', encoding='utf-8') as envfile:
        postgres_env_variables = json.load(envfile)
    # backend_server_ip = backend_server_credentials['backend_server_ip']
    # username = backend_server_credentials['username']
    # password = backend_server_credentials['password']

    postgres_env_variables = PostgresEnvVariables(
        DB_ENGINE=postgres_env_variables['DB_ENGINE'],
        DB_NAME=postgres_env_variables['DB_NAME'],
        POSTGRES_USER=postgres_env_variables['POSTGRES_USER'],
        POSTGRES_PASSWORD=postgres_env_variables['POSTGRES_PASSWORD'],
        DB_HOST=postgres_env_variables['DB_HOST'],
        DB_PORT=postgres_env_variables['DB_PORT'],
        DOMAIN_HOST=postgres_env_variables['DOMAIN_HOST'],
        HOST_PROTOCOL=postgres_env_variables['HOST_PROTOCOL']
    )

    return postgres_env_variables


def get_postgres_env_variables() -> PostgresEnvVariables:
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
    if os.path.exists(get_postgres_env_file_path()):
        postgres_env_variables = read_postgres_env_variables_json()
        # print(
        #         f'\n\'backendservercredentials.json\' file already exists in search path:\n'
        #         f'{get_backend_server_credentials_json_file_path().parent}'
        # )
        # print(f'\nCredentials to establish SSH connection with remote server')
        # print(f'application backend server ip: {backend_server_credentials.backend_server_ip}')
        # print(f'username: {backend_server_credentials.username}')
        # print(f'password: {backend_server_credentials.password}')
    else:
        write_postgres_env_variables_json()
        postgres_env_variables = read_postgres_env_variables_json()
        print(f'\n\'.env\' file saved')
        print(f'\npostgres environment variables\' values from \'.env\' file needed for postgresDB functionality')
        print(f'DB_ENGINE: {postgres_env_variables.DB_ENGINE}')
        print(f'DB_NAME: {postgres_env_variables.DB_NAME}')
        print(f'POSTGRES_USER: {postgres_env_variables.POSTGRES_USER}')
        print(f'POSTGRES_PASSWORD: {postgres_env_variables.POSTGRES_PASSWORD}')
        print(f'DB_HOST: {postgres_env_variables.DB_HOST}')
        print(f'DB_PORT: {postgres_env_variables.DB_PORT}')
        print(f'DOMAIN_HOST: {postgres_env_variables.DOMAIN_HOST}')
        print(f'HOST_PROTOCOL: {postgres_env_variables.HOST_PROTOCOL}')
    return postgres_env_variables


def move_env_docker_compose_files_to_remote() -> None:
    """

    :return:

    """
    # import scp
    from scp import SCPClient

    postgres_env_file_path_local = get_postgres_env_file_path()
    postgres_env_file_name_local = postgres_env_file_name_remote = '.env'
    docker_compose_file_name_local = 'docker-compose_move_2_server.yml'
    docker_compose_file_path_local = get_postgres_env_file_path().parent / docker_compose_file_name_local

    docker_compose_file_name_remote = 'docker-compose.yml'
    # docker_compose_file_path_remote = f'~/tg_bot_constructor/infra/{docker_compose_file_name_remote}'

    remote_directory = '~/tg_bot_constructor/infra/'
    docker_compose_file_path_remote = f'{remote_directory}{docker_compose_file_name_remote}'
    postgres_env_file_path_remote = f'{remote_directory}{postgres_env_file_name_remote}'

    # оставлено для примера отображения прогресса передачи файлов по SCP
    # def progress(filename, size, sent):
    #     sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent) / float(size) * 100))
    # scp = SCPClient(rsa_key_based_connect().get_transport(), progress=progress)

    # SCPCLient takes a paramiko transport and progress callback as its arguments
    scp = SCPClient(rsa_key_based_connect().get_transport())
    # send '.env' and 'docker-compose_move_2_server.yml' files to remote server
    scp.put(postgres_env_file_path_local, postgres_env_file_path_remote)
    scp.put(docker_compose_file_path_local, docker_compose_file_path_remote)
    print(
        f'\n---------------------------------------------------------\n'
        f'\'{postgres_env_file_name_local}\' and \'{docker_compose_file_name_local}\' files,\n'
        f'sent to remote server directory: {remote_directory}'
        f'\n---------------------------------------------------------\n'
    )

    # Should now be printing the current progress of your put function
    scp.close()
