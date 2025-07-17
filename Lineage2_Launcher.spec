# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\main.py'],
    pathex=[],
    binaries=[('C:\\Users\\david\\AppData\\Local\\Programs\\Python\\Python312\\python312.dll', '.')],
    datas=[('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\launcher.json', '.'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets', 'assets'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\config', 'config'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\system', 'system'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\launcher.json', '.'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\main.py', '.'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\__init__.py', '.'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets\\banner.png', 'assets'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets\\bg.png', 'assets'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets\\flag.png', 'assets'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets\\icon.ico', 'assets'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets\\icon.png', 'assets'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\config\\config.py', 'config'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\core\\exceptions.py', 'core'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\core\\launcher.py', 'core'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\core\\system.py', 'core'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\core\\updater.py', 'core'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\core\\__init__.py', 'core'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\services\\game.py', 'services'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\services\\news.py', 'services'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\services\\__init__.py', 'services'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\ui\\launcher_ui.py', 'ui'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\utils\\locale.py', 'utils'), ('e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\utils\\__init__.py', 'utils')],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'requests', 'mega_lite', 'google.auth', 'google.oauth2', 'google_auth_oauthlib', 'google_auth_httplib2', 'googleapiclient', 'core', 'core.updater', 'config', 'config.config', 'services', 'services.news', 'services.game', 'utils', 'utils.locale', 'ui', 'ui.launcher_ui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Lineage2_Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='.',
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['e:\\Telegram Desktop\\Proyectos\\GitHub\\Lineage_2\\git_launcher\\Lineage2\\src\\assets\\icon.ico'],
)
