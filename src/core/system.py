import os
import shutil
import zipfile
from typing import Optional

class SystemManager:
    def __init__(self, system_folder: str):
        self.system_folder = system_folder
        self.version_file = os.path.join(system_folder, 'system_version.txt')

    def get_local_version(self) -> Optional[str]:
        """Get the local system version, handling potential encoding issues."""
        if not os.path.exists(self.version_file):
            return None
        
        try:
            # Use 'utf-8-sig' to handle BOM (Byte Order Mark) if present
            with open(self.version_file, 'r', encoding='utf-8-sig') as f:
                return f.read().strip()
        except (IOError, UnicodeDecodeError) as e:
            return None

    def remove_system(self) -> bool:
        """Remove the system folder and all its contents"""
        try:
            if os.path.exists(self.system_folder):
                shutil.rmtree(self.system_folder)
            return True
        except Exception as e:
            return False

    def extract_system(self, zip_path: str, password: Optional[bytes] = None) -> bool:
        """
        Extracts system files from a zip archive non-destructively.
        It overwrites existing files and adds new ones.
        """
        if not os.path.exists(zip_path) or not zipfile.is_zipfile(zip_path):
            return False

        os.makedirs(self.system_folder, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Check for password protection
                if password:
                    try:
                        zip_ref.extractall(pwd=password)
                    except RuntimeError as e:
                        if 'bad password' in str(e).lower():
                            return False
                        raise
                else:
                    zip_ref.extractall(path=self.system_folder)
            
            return True
        except Exception as e:
            return False

    def set_version(self, version: str) -> bool:
        """Set the system version in the version file"""
        try:
            os.makedirs(self.system_folder, exist_ok=True)
            with open(self.version_file, 'w', encoding='utf-8') as f:
                f.write(version)
            return True
        except Exception as e:
            return False