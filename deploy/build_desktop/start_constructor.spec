# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from enum import Enum
import PyInstaller.config
import os
import sys

# обходное решение для добавления текущей директории в 'PYTHONPATH'
#  небходимо для того, чтобы проходили выполняемые ниже import'ы
sys.path.append(SPECPATH)

from python_venv_execs_paths import get_building_dir

from application_type_enum import ApplicationTypeEnum
from build_executable_utils import read_specfileconf, filename_to_build
from build_executable_utils import suffix_for_app_and_folder_name, app_and_folder_name_without_time_label
from build_executable_utils import time_suffix_for_app_and_folder_name, app_and_folder_name_with_time_label_suffix

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
#    application_project_dir = os.path.normpath(spec_file_dir() / '..' / '..' / 'simple_gram_desktop')
    application_project_dir = (spec_file_dir() / '..' / '..' / 'simple_gram_desktop').resolve()
    return application_project_dir


# working and destination directories for executable file creation
build_dir = get_building_dir() / 'build'
dist_dir = get_building_dir() / 'dist'

build_dir.mkdir(exist_ok=True)
dist_dir.mkdir(exist_ok=True)


# define working directory for executable file creation
PyInstaller.config.CONF['workpath'] = str(build_dir)
# define destination directory for executable file creation
PyInstaller.config.CONF['distpath'] = str(dist_dir)

app_type = read_specfileconf()

a = Analysis(
    [application_project_dir() / filename_to_build(app_type)],
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
    name=app_and_folder_name_with_time_label_suffix(app_type),
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
               name=app_and_folder_name_without_time_label(app_type))
