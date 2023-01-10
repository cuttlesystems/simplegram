# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path


block_cipher = None


a = Analysis(
    ['start_constructor.py'],
    pathex=[
	'.', 
#	'D:\\CuttleSystems\\hidden_hello_world_project\\hidden_hello_world\\abc_bca'
    ],
    binaries=[],
    datas=[(
        Path('desktop_constructor_app') / 'constructor_app' / 'translations' / '*.qm',
        Path('desktop_constructor_app') / 'constructor_app' / 'translations'
    )],
    hiddenimports=['desktop_constructor_app'],
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

#exe = EXE(
#    pyz,
#    a.scripts,
#    a.binaries,
#    a.zipfiles,
#    a.datas,
#    [],
##    name='start_constructor',
#    name='Bot Constructor by Cuttle Systems',
#    debug=False,
#    bootloader_ignore_signals=False,
#    strip=False,
#    upx=True,
#    upx_exclude=[],
#    runtime_tmpdir=None,
#    console=False,
#	icon='.\desktop_constructor_app\constructor_app\images\cuttle_systems.ico',
#    disable_windowed_traceback=False,
#    argv_emulation=False,
#    target_arch=None,
#    codesign_identity=None,
#    entitlements_file=None,
#)


exe = EXE(
    pyz,
    a.scripts,
    [],
	exclude_binaries=True,
#    name='start_constructor',
    name='BotConstructorByCuttleSystems',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
#    console=False,
    console=True,
	icon='.\desktop_constructor_app\constructor_app\images\cuttle_systems.ico',
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
               name='BotConstructorByCuttleSystems')