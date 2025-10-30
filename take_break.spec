# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files

block_cipher = None

# Только нужные данные PySide6 (без всего мусора)
pyside6_datas = collect_data_files('PySide6.QtCore', True)
pyside6_datas += collect_data_files('PySide6.QtGui', True)
pyside6_datas += collect_data_files('PySide6.QtWidgets', True)
pyside6_hiddenimports = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app_data', 'app_data'),
        *pyside6_datas,
    ],
    hiddenimports=[
        'keyboard',
        'requests',
        'PIL',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Исключить весь мусор PySide6
        'PySide6.QtCore.QtCoreTranslations',
        'PySide6.QtGui.translations',
        'PySide6.QtWidgets.translations',
        'PySide6.Qt3D',
        'PySide6.QtCharts',
        'PySide6.QtDataVisualization',
        'PySide6.QtDesigner',
        'PySide6.QtHelp',
        'PySide6.QtLocation',
        'PySide6.QtMultimedia',
        'PySide6.QtNetwork',
        'PySide6.QtNetworkAuth',
        'PySide6.QtNfc',
        'PySide6.QtPdf',
        'PySide6.QtPositioning',
        'PySide6.QtQuick',
        'PySide6.QtQml',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtSensors',
        'PySide6.QtSerialPort',
        'PySide6.QtSql',
        'PySide6.QtSvg',
        'PySide6.QtTest',
        'PySide6.QtUiTools',
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebSockets',
        'PySide6.QtXml',
        'PySide6.scripts',
    ],
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
    name='take_break',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_data/logo/logo.ico',
)

# Фильтровать .qm файлы (переводы)
filtered_datas = [item for item in a.datas if not item[0].endswith('.qm')]

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    filtered_datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='take_break',
)

