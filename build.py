import os
import sys
import shutil
import PyInstaller.__main__
from pathlib import Path

def add_data_files(base_dir, src_dir):
    """Recursively add data files from src_dir."""
    data_files = []
    
    # Lista de archivos y directorios a incluir explícitamente
    include_patterns = [
        '*.py',
        '*.json',
        '*.png',
        '*.ico',
        '*.qss',
        '*.txt',
        '*.md',
        'system/*',  # Incluir todo el directorio system
        'assets/*',  # Incluir todo el directorio assets
        'config/*',  # Incluir todo el directorio config
    ]
    
    # Recorrer el directorio src
    for root, dirs, files in os.walk(src_dir):
        # Omitir directorios no deseados
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.github']]
        
        for file in files:
            # Verificar si el archivo coincide con algún patrón de inclusión
            if any(file.endswith(ext) for ext in ['.pyc', '.pyo', '.pyd', '.so']):
                continue
                
            src_file = Path(root) / file
            rel_path = str(src_file.relative_to(base_dir))
            
            # Determinar el directorio de destino
            if 'src' in rel_path:
                dest_dir = str(Path(rel_path).parent).replace('src', '').strip(os.sep)
            else:
                dest_dir = ''
                
            # Asegurarse de que no haya directorios vacíos
            if dest_dir == '.':
                dest_dir = ''
                
            data_files.append((str(src_file), dest_dir))
    
    return data_files

def main():
    # Ruta base del proyecto
    BASE_DIR = Path(__file__).parent.absolute()
    SRC_DIR = BASE_DIR / 'src'
    
    # Archivo principal de la aplicación
    main_script = SRC_DIR / 'main.py'
    
    # Nombre de la aplicación
    app_name = 'Lineage2_Launcher'
    
    # Directorios de recursos a incluir
    assets_dir = SRC_DIR / 'assets'
    config_dir = SRC_DIR / 'config'
    
    # Obtener todos los archivos de datos recursivamente
    data_files = add_data_files(BASE_DIR, SRC_DIR)
    
    # Construir los argumentos de PyInstaller para un solo archivo
    pyinstaller_args = [
        str(main_script),
        '--name', app_name,
        '--onefile',  # Un solo archivo ejecutable
        '--windowed',
        '--icon', str(assets_dir / 'icon.ico'),
        '--add-binary', f'{Path(sys.executable).parent / "python312.dll"};.',
        '--add-data', f'{SRC_DIR / "launcher.json"};.',
        '--add-data', f'{assets_dir}{os.pathsep}assets',
        '--add-data', f'{config_dir}{os.pathsep}config',
        '--add-data', f'{BASE_DIR / "system"}{os.pathsep}system',
        '--runtime-tmpdir=.',  # Directorio temporal para extraer archivos
    ]
    
    # Agregar archivos de datos con el formato correcto
    for src, dst in data_files:
        # Usar el formato correcto para --add-data: 'source;destination' en Windows
        if dst:  # Si hay un subdirectorio de destino
            arg = f'{src};{dst}'
        else:  # Si va en el directorio raíz
            arg = f'{src};.'
        pyinstaller_args.extend(['--add-data', arg])
    
    # Agregar importaciones ocultas necesarias
    hidden_imports = [
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'requests',
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
        'ui.launcher_ui'
    ]
    
    for imp in hidden_imports:
        pyinstaller_args.extend(['--hidden-import', imp])
    
    # Limpiar builds y dists anteriores
    if (BASE_DIR / 'build').exists():
        shutil.rmtree(BASE_DIR / 'build')
    if (BASE_DIR / 'dist').exists():
        shutil.rmtree(BASE_DIR / 'dist')
    
    print("Iniciando el proceso de construcción...")
    print("Argumentos de PyInstaller:", ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in pyinstaller_args))
    
    # Ejecutar PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n¡Construcción completada!")
    print(f"El ejecutable se encuentra en: {BASE_DIR / 'dist' / f'{app_name}.exe'}")

if __name__ == '__main__':
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller no está instalado.")
        print("Instálalo con: pip install pyinstaller")
        sys.exit(1)
    
    main()
