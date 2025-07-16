# hook-sys.py
# Este hook se utiliza para asegurar que todos los DLLs de Python y dependencias necesarias
# sean correctamente recolectados por PyInstaller, lo que puede resolver errores como
# "Failed to load Python DLL".

from PyInstaller.utils.hooks import collect_dynamic_libs

# Recolecta todas las librerías dinámicas asociadas con el módulo 'sys'.
# Esto obliga a PyInstaller a encontrar y empaquetar el DLL de Python (por ejemplo, python312.dll)
# y cualquier otra librería requerida.
binaries = collect_dynamic_libs('sys')