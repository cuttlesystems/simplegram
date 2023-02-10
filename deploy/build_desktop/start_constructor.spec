# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from enum import Enum
import time
import PyInstaller.config
import os
import sys
#import json
from application_type_enum import ApplicationTypeEnum
from build_executable_utils import read_specfileconf, filename_to_build

# обходное решение для добавления текущей директории в 'PYTHONPATH'
#  небходимо для того, чтобы проходил import, выполняемый строкой ниже
sys.path.append('.')

from python_venv_execs_paths import get_building_dir


block_cipher = None


def spec_file_dir() -> Path:
    """
    define the function to get the 'start_constructor.spec'-file path
    D:\Git Repos\tg_bot_constructor\deploy\build_desktop
    """
    return Path(SPECPATH)


def application_project_dir() -> Path:
    """
    define the function to get the project_directory path
    D:\Git Repos\tg_bot_constructor\simple_gram_desktop
    """
    return spec_file_dir() / Path('..') / '..' / 'simple_gram_desktop'


#def read_specfileconf() -> ApplicationTypeEnum:
#    """
#    read content of 'specfileconf.json' file
#    """
#    with open('specfileconf.json', 'rt', encoding='utf-8') as conffile:
#        specfileconf_content = json.load(conffile)
#        application_type = ApplicationTypeEnum(specfileconf_content['application_type'])
#        print(f'\nconffile: {conffile}')
#        print(f'specfileconf_content: {specfileconf_content}')
#        print(f'application_type: {application_type}')
#        return application_type
#
#
#def filename_to_build() -> str:
#    """
#    define the filename of application used to build an executable
#    """
#    application_type = read_specfileconf()
#    if application_type == ApplicationTypeEnum.CHAMOMILE:
#        filename = 'start_constructor.py'
#    elif application_type == ApplicationTypeEnum.SHIBOKEN:
#        filename = 'start_constructor_shiboken.py'
#    else:
#        raise NotImplementedError(f'Unsupported application type: {application_type}')
#    print(f'\nFilename of application to build an executable: \'{filename}\'\n')
#    return filename


def suffix_for_app_and_folder_name() -> str:
    """
    define suffix for 'simple_gram' application executable name and it's folder name
    """
    application_type = read_specfileconf()
    if application_type == ApplicationTypeEnum.CHAMOMILE:
        suffix = '_chamomile'
    elif application_type == ApplicationTypeEnum.SHIBOKEN:
        suffix = '_shiboken'
    else:
        raise NotImplementedError(f'Unsupported application type: {application_type}')
    print(f'\nSuffix for \'simple_gram\' application executable name and it\'s folder name: \'{suffix}\'\n')
    return suffix


def app_and_folder_name_without_time_label() -> str:
    """
    define 'simple_gram' application executable name and it's folder name without time label
    """
    app_and_folder_name_with_no_time = f'simple_gram{suffix_for_app_and_folder_name()}'
    print(
        f'\n\'simple_gram\' application executable name and it\'s folder name without time label: '
        f'\'{app_and_folder_name_with_no_time}\'\n'
    )
#    print(
#        '\n\'simple_gram\' application executable name and it\'s folder name without time label: ',
#        app_and_folder_name_with_no_time,
#        '\n'
#    )
    return app_and_folder_name_with_no_time


#def app_and_folder_name_without_time_label() -> str:
#    """
#    define 'simple_gram' application executable name and it's folder name without time label
#    """
#    application_type = read_specfileconf()
#    if application_type == ApplicationTypeEnum.CHAMOMILE:
#        app_and_folder_name_with_no_time = 'start_constructor.py'
#    elif application_type == ApplicationTypeEnum.SHIBOKEN:
#        app_and_folder_name_with_no_time = f'simple_gram{suffix_for_app_and_folder_name()}'
#    else:
#        raise NotImplementedError(f'Unsupported application type: {application_type}')
#    print(
#        f'\n\'simple_gram\' application executable name and it\'s folder name without time label:
#         {app_and_folder_name_with_no_time}\n'
#    )
#    return app_and_folder_name_with_no_time


def time_suffix_for_app_and_folder_name() -> str:
    """
    create current time suffix for file/folder name
    """
    time_suffix = '_'+time.strftime("%Y_%m_%d__%H_%M_%S")
    return time_suffix


def app_and_folder_name_with_time_label_suffix() -> str:
    """
    define 'simple_gram' application executable name and it's folder name with time label suffix
    """
    app_and_folder_name_with_time = f'{app_and_folder_name_without_time_label()}{time_suffix_for_app_and_folder_name()}'
    print(
        f'\n\'simple_gram\' application executable name and it\'s folder name with time label: '
        f'\'{app_and_folder_name_with_time}\'\n'
    )
#    print(
#        '\n\'simple_gram\' application executable name and it\'s folder name with time label: ',
#        app_and_folder_name_with_time,
#        '\n'
#    )
#    print(
#        f'\n\'simple_gram\' application executable name and it\'s folder name with time label: '
#        f'{app_and_folder_name_with_time}\n'
#    )
    return app_and_folder_name_with_time


#def app_and_folder_name_with_time_label_suffix() -> str:
#    """
#    define 'simple_gram' application executable name and it's folder name with time label suffix
#    """
#    application_type = read_specfileconf()
#    if application_type == ApplicationTypeEnum.CHAMOMILE:
#        app_and_folder_name_with_time = 'start_constructor.py'
#    elif application_type == ApplicationTypeEnum.SHIBOKEN:
#        app_and_folder_name_with_time = 'start_constructor_shiboken.py'
#        f'simple_gram{suffix_for_app_and_folder_name()}{time_suffix_for_app_and_folder_name()}'
#        app_and_folder_name_without_time_label
#    else:
#        raise NotImplementedError(f'Unsupported application type: {application_type}')
#    print(
#        f'\n\'simple_gram\' application executable name and it\'s folder name with time label:
#         {app_and_folder_name_with_time}\n'
#    )
#    return app_and_folder_name_with_time


# working and destination directories for executable file creation
build_dir = get_building_dir() / 'build'
dist_dir = get_building_dir() / 'dist'

build_dir.mkdir(exist_ok=True)
dist_dir.mkdir(exist_ok=True)


# define working directory for executable file creation
PyInstaller.config.CONF['workpath'] = str(build_dir)
# define destination directory for executable file creation
PyInstaller.config.CONF['distpath'] = str(dist_dir)


a = Analysis(
    [application_project_dir() / filename_to_build()],
    pathex=[
        application_project_dir(),
    ],
    binaries=[],
    datas=[(
        application_project_dir() / 'constructor_app' / 'translations' / '*.qm',
            Path('constructor_app') / 'translations'
    )],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
#    name=f'simple_gram{suffix_for_app_and_folder_name()}_'+time.strftime("%Y_%m_%d__%H_%M_%S"),
#    name=f'simple_gram{suffix_for_app_and_folder_name()}{time_suffix_for_app_and_folder_name()}',
    name=app_and_folder_name_with_time_label_suffix(),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon=str(application_project_dir() / 'constructor_app' / 'images' / 'cuttle_systems.ico'),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
#               name=f'simple_gram{suffix_for_app_and_folder_name()}')
               name=app_and_folder_name_without_time_label())
