# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')

block_cipher = None

a = Analysis(
    ['run_main.py'],
    pathex=['.'],
    binaries=streamlit_binaries + [],
    datas=streamlit_datas + [
        ('MuonDetector.py', '.'),
            ],
    hiddenimports=streamlit_hiddenimports + [
        'pandas',
        'numpy',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'scipy',
        'scipy.optimize',
        'scipy.stats',
        'scipy.special',
        'scipy.special._ufuncs',
        'scipy._lib.messagestream',
        'scipy.sparse.csgraph._validation',
        'PIL',
        'PIL._tkinter_finder',
        'altair',
        'toml',
        'tornado',
        'tornado.ioloop',
        'tornado.web',
        'tornado.websocket',
        'pyarrow',
        'git',
        'gitdb',
        'smmap',
        'click',
        'importlib_metadata',
        'packaging',
        'jinja2',
        'jsonschema',
        'requests',
        'urllib3',
    ],
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
    name='MuonDetector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MuonDetector',
)
