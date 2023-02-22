"""
модуль с дополнительными функциями, которые используются при создании исполняемого файла приложения 'simple_gram'
"""
import json

from application_type_enum import ApplicationTypeEnum

import time


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


def filename_to_build(app_type: ApplicationTypeEnum) -> str:
    """
    define the filename of application used to build an executable
    Returns: the filename - 'start_constructor.py' or 'start_constructor_shiboken.py' -
     to build 'simple_gram' application executable from

    """
    application_type = app_type
    if application_type == ApplicationTypeEnum.CHAMOMILE:
        filename = 'start_constructor.py'
    elif application_type == ApplicationTypeEnum.SHIBOKEN:
        filename = 'start_constructor_shiboken.py'
    else:
        raise NotImplementedError(f'Unsupported application type: {application_type}')
    print(f'\nScript filename to build an executable: \'{filename}\'\n')
    return filename


def suffix_for_app_and_folder_name(application_type: ApplicationTypeEnum) -> str:
    """
    define suffix for 'simple_gram' application executable name and it's folder name
    """
    if application_type == ApplicationTypeEnum.CHAMOMILE:
        suffix = '_chamomile'
    elif application_type == ApplicationTypeEnum.SHIBOKEN:
        suffix = '_shiboken'
    else:
        raise NotImplementedError(f'Unsupported application type: {application_type}')
    return suffix


def app_and_folder_name_without_time_label(app_type: ApplicationTypeEnum) -> str:
    """
    define 'simple_gram' application executable name and it's folder name without time label
    """
    app_and_folder_name_with_no_time = f'simple_gram{suffix_for_app_and_folder_name(app_type)}'
    return app_and_folder_name_with_no_time


def time_suffix_for_app_and_folder_name() -> str:
    """
    create current time suffix for file/folder name
    """
    time_suffix = '_' + time.strftime("%Y_%m_%d__%H_%M_%S")
    return time_suffix


def app_and_folder_name_with_time_label_suffix(app_type: ApplicationTypeEnum) -> str:
    """
    define 'simple_gram' application executable name or it's folder name with time label suffix
    """
    app_and_folder_name_with_time = \
        f'{app_and_folder_name_without_time_label(app_type)}{time_suffix_for_app_and_folder_name()}'
    print(
        f'\n\'simple_gram\' application executable name with application type suffix and time label: '
        f'\'{app_and_folder_name_with_time}\'\n'
    )
    return app_and_folder_name_with_time
