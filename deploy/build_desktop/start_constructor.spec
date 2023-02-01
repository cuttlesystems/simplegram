# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from enum import Enum
import time
import PyInstaller.config
import os
import sys

# обходное решение для добавления текущей директории в 'PYTHONPATH'
#  небходимо для того, чтобы проходил import, выполняемый строкой ниже
sys.path.append('.')

#from python_and_venv_path import get_building_dir
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
    [application_project_dir() / 'start_constructor.py'],
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
    name='simple_gram_'+time.strftime("%Y_%m_%d__%H_%M_%S"),
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
               name='simple_gram')