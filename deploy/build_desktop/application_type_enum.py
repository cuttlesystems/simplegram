from enum import Enum


class ApplicationTypeEnum(Enum):
    CHAMOMILE = 'CHAMOMILE'
    SHIBOKEN = 'SHIBOKEN'


if __name__ == '__main__':
    print(f'\n{ApplicationTypeEnum.CHAMOMILE.name}')
    print(f'{ApplicationTypeEnum.CHAMOMILE.value}')
    print(f'\n{ApplicationTypeEnum.SHIBOKEN.name}')
    print(f'{ApplicationTypeEnum.SHIBOKEN.value}')

    print(f'\n{list(ApplicationTypeEnum)}')
