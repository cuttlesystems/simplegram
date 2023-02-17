import subprocess
from subprocess import run
from pathlib import Path
# модуль для определения пути к исполняемому файлу установленного в системе python
import shutil

import docker

from get_repo_to_deploy_from import get_repo_to_deploy
from deploy_server_utils import get_docker_registry_credentials, docreg_login_locally, docreg_logout_locally, \
    get_postgres_env_variables, convert_postgres_env_variables_json_to_text, docker_create_image_locally, \
    docker_tag_local_image_to_push, docker_push_tagged_local_image_to_registry, delete_infra_web_latest_image_remotely
from deploy_server_utils import get_postgres_env_file_path, move_env_docker_compose_files_to_remote
from deploy_server_utils import move_rsa_pub_key_to_remote
# from deploy_server_utils import rsa_key_based_connect
from deploy_server_utils import get_backend_server_credentials, gen_ssh_key_pair
# from deploy_server_utils import add_pub_key_to_remote_server
from deploy_server_utils import docreg_login_remotely


def check_git_python_is_installed() -> bool:
    try:
        import git
        is_installed = True
    except ImportError:
        is_installed = False
    return is_installed


def install_git_module() -> None:
    run(['pip', 'install', 'gitpython'])
    print(f'\'gitpython\' module is installed')


def check_docker_is_installed() -> bool:
    try:
        import docker
        is_installed = True
    except ImportError:
        is_installed = False
    return is_installed


def install_docker_module() -> None:
    run(['pip', 'install', 'docker'])
    print(f'\'docker\' module is installed')


def check_paramiko_is_installed() -> bool:
    """
    define function to check whether the 'paramiko' package
    which is used to enable ssh:// support for Docker daemon connection
    :return:
    """
    try:
        import paramiko
        is_installed = True
    except ImportError:
        is_installed = False
    return is_installed


def install_paramiko_module() -> None:
    run(['pip', 'install', 'paramiko'])
    print(f'\'paramiko\' module is installed')


if __name__ == '__main__':
    # определение пути к исполняемому файлу python в системе
    system_python_path = shutil.which('python')
    print('\nПуть к исполняемому файлу python в системе: ', shutil.which('python'), '\n')

    # run([get_venv_python_path(venv_dir), '-m', 'pip', 'install', '--upgrade', 'pip'])
    # run(['../venv/Scripts/python.exe', '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([f'{system_python_path}', '-m', 'pip', 'install', '--upgrade', 'pip'])
    print(f'\n\'git\' module is installed: {check_git_python_is_installed()}')
    print(f'\n\'docker\' module is installed: {check_docker_is_installed()}')
    print(f'\n\'paramiko\' module is installed: {check_paramiko_is_installed()}')

    # install 'GitPython' module if not installed yet
    if not check_git_python_is_installed():
        install_git_module()

    # install 'docker' module if not installed yet
    if not check_docker_is_installed():
        install_docker_module()

    # install 'paramiko' module if not installed yet
    if not check_paramiko_is_installed():
        install_paramiko_module()

    # from subprocess import Popen, PIPE
    result = subprocess.Popen(['pip', 'list'], text=True, stdout=subprocess.PIPE)
    # result = subprocess.Popen(['pip', 'list'], stdout=subprocess.PIPE)
    # result.stdout
    # result.stderr
    pip_output_str = result.stdout.read()

    print(f'\nresult.stdout: ', pip_output_str)

    with open('pip_list.txt', 'w') as file:
        file.write(pip_output_str)
        file.writelines('add any str 123')

    repo_to_deploy = get_repo_to_deploy()
    repo = repo_to_deploy.repository
    branch = repo_to_deploy.branch
    commit = repo_to_deploy.commit
    print(
        '\n\'tg_bot_constructor\' server application will be deployed from'
        '\n    repository: ', repo,
        '\n    branch: ', branch,
        '\n    commit: ', commit
    )
    project_dir = Path('.') / repo

    import git
    from git import Repo

    # define parameters for a request to GitHub
    # Personal Access Token (PAT) for authorization in GitHub repo
    token = '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'
    # organization in GitHub the repository belongs to
    owner = 'cuttlesystems'
    # repo = 'tg_bot_constructor'
    path = 'README.md'

    HTTPS_REMOTE_URL = f'https://{token}:x-oauth-basic@github.com/{owner}/{repo}'
    if not project_dir.exists():
        # repo = git.Repo(project_dir)
        print(f'\nproject_dir: ', project_dir)
        print(f'\nLocal repository: ', repo)
        # URL 4 cloning a private repo using HTTPS with GitPython
        HTTPS_REMOTE_URL = f'https://{token}:x-oauth-basic@github.com/{owner}/{repo}'
        print(f'\nURL 4 cloning a private repo using HTTPS with gitpython: {HTTPS_REMOTE_URL}')
        Repo.clone_from(
            f'{HTTPS_REMOTE_URL}',
            project_dir
        )
        repo = git.Repo(project_dir)
        print(f'Active branch: {repo.active_branch}')
        print(f'All branches: {repo.branches}\n')
        origin = repo.remote(name='origin')
        print(f'\nRemote repository: ', origin)
        print(f'\nrepo.remotes: ', repo.remotes)
        print('Branches:')
        for branch in repo.branches:
            print(branch)
        # Reference a remote by its name as part of the object
        print(f'\nRemote name: {repo.remotes.origin.name}')
        print(f'Remote URL: {repo.remotes.origin.url}')
        # repo.git.checkout('origin')
        print(f'Active branch: {repo.active_branch}')
    else:
        repo = git.Repo(project_dir)

        try:
            active_branch = repo.active_branch
        except TypeError:
            # branch is in detached state
            active_branch = None
            active_branch_name = None
        print(f'\nActive branch: {active_branch}')
        print(f'User branch input: {branch}')
        # active_branch_name = None
        if active_branch is not None:
            active_branch_name = active_branch.name
        else:
            print(f'\nCurrently HEAD is a detached symbolic reference')

        if not branch == active_branch_name:
            print(f'\nSelected branch to deploy from: {branch}')
            print(f'Switching to selected branch: {branch}')

            print(f'\nSwitched to selected branch to deploy from: {branch}')
            repo.git.checkout(f'{branch}')
            print(f'Current active branch is: {repo.active_branch}')

        print(f'\nproject_dir: ', project_dir)
        print(f'\nLocal repository: ', repo)
        print(f'\nURL 4 cloning a private repo using HTTPS with gitpython: {HTTPS_REMOTE_URL}')
        origin = repo.remote(name='origin')
        print(f'\nRemote repository: ', origin)
        print(f'\nrepo.remotes: ', repo.remotes)
        # print(f'\nAll branches: {repo.branches}\n')
        print(f'\nAll branches:')
        for branch in repo.branches:
            print(f'- {branch.name}')
        remote_refs = repo.remote().refs
        print(f'\nremote_refs names:')
        for refs in remote_refs:
            print(f'remote_ref: {refs.name}')

        print(f'\nRemote name: {repo.remotes.origin.name}')
        print(f'Remote URL: {repo.remotes.origin.url}')

        print(f'Current active branch is: {repo.active_branch}')

        origin.pull()
        print(f'\nGit pull from \'{origin}/{branch}\' completed\n')

    # credentials to establish SSH connection with remote server where the application backend is deployed
    backend_server_credentials = get_backend_server_credentials()

    # get credentials saved to 'dockerregistrycredentials.json' file to log in private docker registry
    docker_registry_credentials = get_docker_registry_credentials()

    # get values from '.env' file
    # echo
    # 'DB_ENGINE=django.db.backends.postgresql
    # DB_NAME=bot_constructor
    # POSTGRES_USER=postgres
    # POSTGRES_PASSWORD=zarFad-huqdit-qavry0
    # DB_HOST=172.21.0.1
    # DB_PORT=5432
    # DOMAIN_HOST=ramasuchka.kz
    # HOST_PROTOCOL=https' > ./$GH_REPO/deploy/deploy_server/infra/.env
    # echo ""
    # echo "'.env-файл' создан в директории '$GH_REPO/deploy/deploy_server/infra/'"
    # echo ""
    postgres_env_file_path = get_postgres_env_file_path()
    print(f'postgres_env_file path: {postgres_env_file_path}')
    # get_postgres_env_variables() - создание '.env_json' файла с переменными окружения для базы данных postgres
    #  в json-формате, а также файла '.env' на его основе с записью необходимых переменных окружения в строковом виде
    convert_postgres_env_variables_json_to_text()


    # copy modified 'docker-compose.yml' file to remote server
    # # scp -r ~/tg_bot_constructor/infra/docker-compose_move_2_server.yml ubuntu@185.146.3.196:~/tg_bot_constructor/infra/docker-compose.yml
    # scp -r ~/tg_bot_constructor/deploy/deploy_server/infra/docker-compose_move_2_server.yml ubuntu@185.146.3.196:~/tg_bot_constructor/infra/docker-compose.yml
    #
    # # copy modified '.env' file to remote server
    # # scp -r ~/tg_bot_constructor/infra/.env ubuntu@185.146.3.196:~/tg_bot_constructor/infra/.env
    # scp -r ~/tg_bot_constructor/deploy/deploy_server/infra/.env ubuntu@185.146.3.196:~/tg_bot_constructor/infra/.env
    move_env_docker_compose_files_to_remote(backend_server_credentials)

    # not necessary
    # add_key_to_known_hosts()
    # rsa_key_based_connect()

    # generate SSH key pair before remote Docker daemon usage if keys don't exist yet
    gen_ssh_key_pair()

    # add_pub_key_to_remote_server()
    move_rsa_pub_key_to_remote(backend_server_credentials)

    # private docker registry logging in locally with credentials
    #  saved to 'dockerregistrycredentials.json' file to push docker image
    docreg_login_locally(docker_registry_credentials)

    # create docker image locally through 'subprocess.run( )' to push it into private docker registry later
    #  sudo docker-compose build --no-cache web
    docker_create_image_locally()

    # tag local 'infra-web' docker image as 'ramasuchka.kz:4443/infra-web:latest' through 'subprocess.run( )'
    #  to push it into private docker registry
    #  sudo docker tag infra-web ramasuchka.kz:4443/infra-web:latest
    # закоменчено, потому что вызов осуществляется в другой функции
    # docker_tag_local_image_to_push()

    # sudo docker push ramasuchka.kz:4443/infra-web:latest
    #
    # echo "Updated 'infra-web' image was pushed to the Private Docker Registry as 'ramasuchka.kz:4443/infra-web:latest'"
    docker_push_tagged_local_image_to_registry()

    # private docker registry logging out locally
    docreg_logout_locally(docker_registry_credentials)

    # exit(0)

    # private docker registry logging in remotely through DockerClient with credentials saved to
    #  'dockerregistrycredentials.json' file to pull docker image
    docreg_login_remotely(backend_server_credentials, docker_registry_credentials)

    # DOCKER STEPS ON REMOTE SERVER
    # recreate_restart_infra_web_container_migrate.sh
    # echo "recreation of a container started"
    # ssh ubuntu@185.146.3.196 'bash -s' < ~/scripts/pull_updated_infra_web_image_restart_container.sh

    # 1 # to avoid multi '<none>' images on the server we should remove 'infra-web:latest' image
    #       before pull update for it from the registry
    # #     '-f' force removing option
    #   sudo docker rmi -f infra-web:latest
    #
    delete_infra_web_latest_image_remotely(backend_server_credentials)

    # 2 # to avoid multi '<none>' images on the server we should remove 'ramasuchka.kz:4443/infra-web:latest' image
    #       before pull update for it from the registry
    # #     '-f' force removing option
    #   sudo docker rmi -f ramasuchka.kz:4443/infra-web:latest
    #
    # 3 # pull updated image from the registry
    #   sudo docker pull ramasuchka.kz:4443/infra-web:latest
    #
    # 4 # tag updated image as 'infra-web:latest'
    #   sudo docker tag ramasuchka.kz:4443/infra-web:latest infra-web:latest

    # remote docker registry logout
    # ssh ubuntu@185.146.3.196 'sudo docker logout https://ramasuchka.kz:4443'
