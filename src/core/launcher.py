import os
import sys
import tempfile
import shutil
from typing import Dict, Optional
import requests
from mega_downloader import download_mega_file

class Launcher:
    def __init__(self, config: Dict):
        self.config = config
        self.temp_dir = None
        
    def get_launcher_version(self) -> Optional[str]:
        """Get the current launcher version"""
        return self.config.get('LauncherVersion', '')

    def update_launcher(self, update_url: str, version: str) -> bool:
        """Update the launcher executable"""
        try:
            is_frozen = getattr(sys, 'frozen', False)
            
            if not is_frozen:
                self.temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
            else:
                self.temp_dir = tempfile.mkdtemp()
            
            new_launcher_path = os.path.join(self.temp_dir, 'launcher_new.exe')
            
            # Download new launcher
            if 'mega.nz' in update_url:
                print(f"[INFO] Descargando launcher de Mega.nz: {update_url}")
                new_launcher = download_mega_file(update_url, self.temp_dir)
                shutil.move(new_launcher, new_launcher_path)
            else:
                print(f"[INFO] Descargando launcher de URL directa: {update_url}")
                r = requests.get(update_url, stream=True)
                with open(new_launcher_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            if not is_frozen:
                # Development mode: notify user to manually copy
                print("[INFO] Modo desarrollo: El nuevo launcher.exe se ha descargado en la carpeta temporal.")
                return True

            # Production mode: create batch file for replacement
            bat_path = os.path.join(self.temp_dir, 'replace_launcher.bat')
            with open(bat_path, 'w') as bat:
                bat.write(f"timeout /t 2\ndel \"{sys.argv[0]}\"\nmove /Y \"{new_launcher_path}\" \"{sys.argv[0]}\"\nstart \"\" \"{sys.argv[0]}\"\n")
            
            print("[INFO] Iniciando reemplazo del launcher...")
            os.startfile(bat_path)
            return True

        except Exception as e:
            print(f"[ERROR] Error actualizando launcher: {e}")
            return False

    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Error cleaning up temp files: {e}")