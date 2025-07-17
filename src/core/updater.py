import requests
import tempfile
import shutil
import zipfile
import os
import sys
from typing import Dict, Optional, Callable
from core.system import SystemManager
from PyQt5 import QtWidgets

def get_base_path():
    """Get the base path for the application."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as a script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
class Updater:
    def __init__(self, config: Dict):
        self.config = config
        self.status = None
        base_path = get_base_path()
        system_path = os.path.join(base_path, 'system')
        self.system_manager = SystemManager(system_path)
        
        # Debug: Print paths
        if self.status:
            self.status(f'Ruta base: {base_path}')
            self.status(f'Ruta del sistema: {system_path}')

    def check_updates(self, status_callback: callable) -> bool:
        """
        Check for launcher and system updates.
        Returns True if an update was performed, False otherwise.
        """
        self.status = status_callback
        try:
            version_data = self._fetch_version_data()
            if not version_data:
                self.status('No se pudo verificar la versión remota.')
                return False

            # Check launcher update
            if self._check_launcher_update(version_data):
                return True  # Update was performed

            # Check system update
            if self._check_system_update(version_data):
                return True  # Update was performed
            
            # If we reach here, no updates were needed
            self.status('El cliente está actualizado.')
            return False

        except Exception as e:
            self.status(f'Error al comprobar actualizaciones: {str(e)}')
            return False

    def _fetch_version_data(self) -> Optional[Dict]:
        """Fetch version data from remote source"""
        try:
            version_url = self.config.get('VersionJsonUrl', '').strip()
            self.status('Comprobando actualizaciones...')
            r = requests.get(version_url, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            self.status('No se pudo obtener version.json remoto.')
            return None

    def _check_launcher_update(self, version_data: Dict) -> bool:
        """Check and update launcher if needed"""
        local_version = self.config.get('LauncherVersion', '')
        remote_version = version_data.get('launcher', {}).get('version', '')
        update_url = version_data.get('launcher', {}).get('url', '')

        if local_version != remote_version and update_url:
            return self._update_launcher(update_url, remote_version)
        return False

    def _check_system_update(self, version_data: Dict) -> bool:
        """Check and update system if needed"""
        remote_version = version_data.get('system', {}).get('version', '')
        update_url = version_data.get('system', {}).get('url', '')

        if not remote_version or not update_url:
            return False

        local_version = self.system_manager.get_local_version()
        
        # Update if local version is missing or different from remote
        if local_version != remote_version:
            return self._update_system(update_url, remote_version)
            
        return False

    def _update_launcher(self, update_url: str, version: str) -> bool:
        """Update launcher executable"""
        try:
            self.status('Actualizando launcher...')
            is_frozen = getattr(sys, 'frozen', False)
            
            if not is_frozen:
                temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
            else:
                temp_dir = tempfile.mkdtemp()
            
            new_launcher_path = os.path.join(temp_dir, 'launcher_new.exe')
            
            if 'mega.nz' in update_url:
                from mega_downloader import download_mega_file
                new_launcher = download_mega_file(update_url, temp_dir)
                shutil.move(new_launcher, new_launcher_path)
            else:
                r = requests.get(update_url, stream=True)
                with open(new_launcher_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            if not is_frozen:
                self.status('Modo desarrollo: El nuevo launcher.exe se ha descargado en la carpeta temporal.')
                QtWidgets.QMessageBox.information(
                    None, "Actualización descargada",
                    f"El nuevo launcher.exe se ha descargado en:\n{new_launcher_path}\n\nCopia manualmente este archivo si deseas probar la actualización."
                )
                return True

            # Production: Create bat for replacement
            bat_path = os.path.join(temp_dir, 'replace_launcher.bat')
            with open(bat_path, 'w') as bat:
                bat.write(f"timeout /t 2\ndel \"{sys.argv[0]}\"\nmove /Y \"{new_launcher_path}\" \"{sys.argv[0]}\"\nstart \"\" \"{sys.argv[0]}\"\n")
            
            os.startfile(bat_path)
            QtWidgets.QApplication.quit()
            sys.exit()
            return True

        except Exception as e:
            self.status(f'Error actualizando launcher: {e}')
            return False

    def _update_system(self, update_url: str, version: str) -> bool:
        """Downloads and extracts the system update using SystemManager."""
        temp_dir = None
        try:
            self.status(f"Descargando System v{version}...")

            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, 'system_update.zip')

            # Download the file
            if 'mega.nz' in update_url:
                from mega_downloader import download_mega_file
                # Asumimos que download_mega_file descarga el archivo y lo nombra como el último componente de la URL
                # y lo deja en temp_dir. Necesitamos moverlo a zip_path.
                downloaded_file_path = download_mega_file(update_url, temp_dir)
                if downloaded_file_path:
                    shutil.move(downloaded_file_path, zip_path)
                else:
                    raise Exception("Fallo la descarga desde Mega.nz")
            else:
                r = requests.get(update_url, stream=True, timeout=60)
                r.raise_for_status()
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Extract the system
            self.status('Descomprimiendo archivos del sistema...')
            if not self.system_manager.extract_system(zip_path, password=b'12345'):
                self.status('Error al descomprimir los archivos del sistema.')
                return False

            # Set the new version
            if not self.system_manager.set_version(version):
                self.status('Error al guardar la nueva versión del sistema.')
                return False

            self.status(f"Sistema actualizado a la versión {version}.")
            return True

        except requests.RequestException as e:
            self.status('Error de red al descargar la actualización.')
            return False
        except Exception as e:
            self.status(f'Error inesperado: {e}')
            return False
        finally:
            # Clean up the temporary directory
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)