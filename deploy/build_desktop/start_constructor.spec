# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import time


block_cipher = None

# define the function to get the 'start_constructor.spec'-file path
# D:\Git Repos\tg_bot_constructor\deploy\build_desktop
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


a = Analysis(
    [application_project_dir() / 'start_constructor.py'],
    pathex=[
        application_project_dir(),
    ],
    binaries=[],
    datas=[(
        application_project_dir() / 'constructor_app' / 'translations' / '*.qm', \
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