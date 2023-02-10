"""
модуль с дополнительными функциями, которые используются при создании исполняемого файла приложения 'simple_gram'
"""
import json

from application_type_enum import ApplicationTypeEnum


def read_specfileconf() -> ApplicationTypeEnum:
    """
    read content of 'specfileconf.json' file
    Returns: 'simple_gram' application type from 'specfileconf.json' file

    """
    with open('specfileconf.json', 'rt', encoding='utf-8') as conffile:
        specfileconf_content = json.load(conffile)
        application_type = ApplicationTypeEnum(specfileconf_content['application_type'])
        print(f'\nconffile: {conffile}')
        print(f'specfileconf_content: {specfileconf_content}')
        print(f'application_type: {application_type}')
        return application_type


def filename_to_build() -> str:
    """
    define the filename of application used to build an executable
    Returns: the filename - 'start_constructor.py' or 'start_constructor_shiboken.py' -
     to build 'simple_gram' application executable from

    """
    application_type = read_specfileconf()
    if application_type == ApplicationTypeEnum.CHAMOMILE:
        filename = 'start_constructor.py'
    elif application_type == ApplicationTypeEnum.SHIBOKEN:
        filename = 'start_constructor_shiboken.py'
    else:
        raise NotImplementedError(f'Unsupported application type: {application_type}')
    print(f'\nFilename of application to build an executable: \'{filename}\'\n')
    return filename
