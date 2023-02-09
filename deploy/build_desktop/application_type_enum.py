from enum import Enum


class ApplicationTypeEnum(Enum):
    CLASSIC = 'CLASSIC'
    SHIBOKEN = 'SHIBOKEN'


if __name__ == '__main__':
    print(f'\n{ApplicationTypeEnum.CLASSIC.name}')
    print(f'{ApplicationTypeEnum.CLASSIC.value}')
    print(f'\n{ApplicationTypeEnum.SHIBOKEN.name}')
    print(f'{ApplicationTypeEnum.SHIBOKEN.value}')

    print(f'\n{list(ApplicationTypeEnum)}')
