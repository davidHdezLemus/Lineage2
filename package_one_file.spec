# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Obtener la ruta base del proyecto
base_dir = os.path.abspath('.')
src_dir = os.path.join(base_dir, 'src')

# Archivos de datos a incluir
datas = [
    (os.path.join(src_dir, 'assets'), 'assets'),
    (os.path.join(src_dir, 'config'), 'config'),
    (os.path.join(base_dir, 'system'), 'system'),
    (os.path.join(src_dir, 'launcher.json'), '.')
]

# Incluir certificados SSL para requests
import requests.certs
cafile = requests.certs.where()
datas.append((cafile, 'certifi'))

# Incluir módulos ocultos necesarios
hidden_imports = [
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'requests',
    'urllib3',
    'urllib3.util',
    'urllib3.util.ssl_',
    'urllib3.packages',
    'urllib3.contrib',
    'urllib3.contrib.pyopenssl',
    'idna',
    'chardet',
    'certifi',
    'mega_lite',
    'google.auth',
    'google.oauth2',
    'google_auth_oauthlib',
    'google_auth_httplib2',
    'googleapiclient',
    'core',
    'core.updater',
    'config',
    'config.config',
    'services',
    'services.news',
    'services.game',
    'utils',
    'utils.locale',
    'ui',
    'ui.launcher_ui',
    'csv',
    'io',
    'json',
    'ssl'
]

# Obtener archivos de datos adicionales de los paquetes
for package in ['PyQt5', 'google', 'requests', 'mega_lite']:
    datas += collect_data_files(package)

# Configuración de análisis
a = Analysis(
    ['src/main.py'],
    pathex=[base_dir, src_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
    optimize=0,
)

# Crear PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Configuración del ejecutable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Lineage2_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(src_dir, 'assets', 'icon.ico')
)
