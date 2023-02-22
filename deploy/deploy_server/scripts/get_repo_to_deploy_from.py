from dataclasses import dataclass


@dataclass(slots=True)
class RepoToDeploy:
    repository: str
    branch: str
    commit: str


def get_repo_to_deploy() -> RepoToDeploy:
    # get repository, branch and commit from user to deploy an app from
    choice_to_deploy_from = input(
        '\n'
        'Where do you want to deploy from:'
        '\n1 (or \'Enter\') - the latest commit from \'main\' branch of "tg_bot_constructor" repository'
        '\n2 - the latest commit from a specific branch of "tg_bot_constructor" repository'
        '\n3 - a specific commit in "tg_bot_constructor" repository'
        '\n4 - a specific commit in specific repository'
        '\n\nInput number to make a choice: '
    )

    if choice_to_deploy_from == '1' or choice_to_deploy_from == '':
        print('\nYou\'ve chosen default repository settings for deployment')
        repo_to_deploy = RepoToDeploy(
            repository='tg_bot_constructor',
            branch='main',
            commit='latest commit'
        )
    elif choice_to_deploy_from == '2':
        repo_to_deploy = RepoToDeploy(
            repository='tg_bot_constructor',
            branch=input('Enter branch to deploy from (push \'Enter\' for default branch - "main"): '),
            commit='latest commit'
        )
        if repo_to_deploy.branch == '':
            repo_to_deploy.branch = 'main'
    elif choice_to_deploy_from == '3':
        # if user chooses a specific commit in "tg_bot_constructor" repository (case №3)
        #  then he doesn't need to input 'branch' value
        repo_to_deploy = RepoToDeploy(
            repository='tg_bot_constructor',
            branch='',
            commit=input(
                'Enter commit hash to deploy from (push \'Enter\' for default - latest commit in \'main\' branch): ')
        )
        if repo_to_deploy.commit == '':
            repo_to_deploy.branch = 'main'
            repo_to_deploy.commit = 'latest commit'
            print('\nYou\'ve chosen default repository settings for deployment')
    else:
        # if user chooses a specific commit in specific repository (case №4)
        #  then he doesn't need to input 'branch' value
        repo_to_deploy = RepoToDeploy(
            repository=input(
                'Enter repository name to deploy from '
                '(push \'Enter\' for default repository name - "tg_bot_constructor"):'
            ),
            branch='',
            commit=input(
                'Enter commit hash to deploy from (push \'Enter\' for default - latest commit in \'main\' branch): '
            )
        )
        if repo_to_deploy.repository == '':
            repo_to_deploy.repository = 'tg_bot_constructor'

        if repo_to_deploy.commit == '':
            repo_to_deploy.branch = 'main'
            repo_to_deploy.commit = 'latest commit'
            print('\nYou\'ve chosen default repository settings for deployment')

    # print(
    #     'tg_bot_constructor app will be deployed from'
    #     '\n    repository: ', repo_to_deploy.repository,
    #     '\n    branch: ', repo_to_deploy.branch,
    #     '\n    commit: ', repo_to_deploy.commit
    # )

    with open('repo_data.txt', 'w') as file:
        # file.write(pip_output_str)
        file.writelines(f'repository: {repo_to_deploy.repository}\n')
        file.writelines(f'branch: {repo_to_deploy.branch}\n')
        file.writelines(f'commit: {repo_to_deploy.commit}\n')
        file.writelines('add any str 123\n')

    return repo_to_deploy


# if __name__ == '__main__':
#     res: RepoToDeploy = get_repo_to_deploy()
#     print('\n', isinstance(res, RepoToDeploy))
#     print('\n', res.repository, res.branch, res.commit)
#     print(
#         '\ntg_bot_constructor app will be deployed from'
#         '\n    repository: ', res.repository,
#         '\n    branch: ', res.branch,
#         '\n    commit: ', res.commit
#     )
