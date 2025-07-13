import sys
import os
import json
import requests
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Multi-idioma
LANGS = {
    'es': {
        'start': 'JUGAR',
        'checking': 'Comprobando actualizaciones...',
        'updating': 'Actualizando archivos...',
        'ready': 'Listo para jugar',
        'update_failed': 'No se pudo conectar con el servidor de actualizaciones.',
    },
    'en': {
        'start': 'PLAY',
        'checking': 'Checking updates...',
        'updating': 'Updating files...',
        'ready': 'Ready to play',
        'update_failed': 'Could not connect to the update server.',
    }
}

class Launcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.lang = self.load_lang_setting()
        self.setWindowTitle(self.config['LauncherTitle'])
        self.setFixedSize(640, 420)
        self.setWindowIcon(QtGui.QIcon(resource_path('assets/icon.png')))
        self.init_ui()
        QtCore.QTimer.singleShot(500, self.check_updates)

    def load_config(self):
        with open(resource_path('launcher.json'), 'r', encoding='utf-8') as f:
            return json.load(f)

    def check_updates(self):
        import tempfile
        import shutil
        import zipfile
        import io
        try:
            VERSION_JSON_URL = self.config.get('VersionJsonUrl', '').strip()
            self.status.setText('Comprobando actualizaciones...')
            QtWidgets.QApplication.processEvents()
            r = requests.get(VERSION_JSON_URL, timeout=10)
            r.raise_for_status()
            version_data = r.json()
        except Exception as e:
            self.status.setText('No se pudo obtener version.json remoto.')
            return

        # --- 1. Comprobar launcher ---
        local_launcher_version = self.config.get('LauncherVersion', '')
        remote_launcher_version = version_data.get('launcher', {}).get('version', '')
        launcher_url = version_data.get('launcher', {}).get('url', '')
        if local_launcher_version != remote_launcher_version and launcher_url:
            self.status.setText('Actualizando launcher...')
            QtWidgets.QApplication.processEvents()
            is_frozen = getattr(sys, 'frozen', False)
            if not is_frozen:
                temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
                os.makedirs(temp_dir, exist_ok=True)
            else:
                temp_dir = tempfile.mkdtemp()
            new_launcher_path = os.path.join(temp_dir, 'launcher_new.exe')
            try:
                if 'mega.nz' in launcher_url:
                    try:
                        from mega_downloader import download_mega_file
                    except ImportError:
                        import subprocess
                        subprocess.run([sys.executable, '-m', 'pip', 'install', 'mega-lite'])
                        from mega_downloader import download_mega_file
                    new_launcher = download_mega_file(launcher_url, temp_dir)
                    shutil.move(new_launcher, new_launcher_path)
                else:
                    r = requests.get(launcher_url, stream=True)
                    with open(new_launcher_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
            except Exception as e:
                self.status.setText(f'Error actualizando launcher: {e}')
                return
            is_frozen = getattr(sys, 'frozen', False)
            if not is_frozen:
                self.status.setText('Modo desarrollo: El nuevo launcher.exe se ha descargado en la carpeta temporal. No se realiza reemplazo automático.')
                QtWidgets.QMessageBox.information(self, "Actualización descargada", f"El nuevo launcher.exe se ha descargado en:\n{new_launcher_path}\n\nCopia manualmente este archivo si deseas probar la actualización.")
                return
            # Producción: Crear bat para reemplazo
            bat_path = os.path.join(temp_dir, 'replace_launcher.bat')
            with open(bat_path, 'w') as bat:
                bat.write(f"timeout /t 2\ndel \"{sys.argv[0]}\"\nmove /Y \"{new_launcher_path}\" \"{sys.argv[0]}\"\nstart \"\" \"{sys.argv[0]}\"\n")
            os.startfile(bat_path)
            QtWidgets.QApplication.quit()
            sys.exit()


        # --- 2. Comprobar system ---
        remote_system_version = version_data.get('system', {}).get('version', '')
        system_url = version_data.get('system', {}).get('url', '')
        system_folder = os.path.join(os.getcwd(), 'system')
        local_version_path = os.path.join(system_folder, 'system_version.txt')
        local_version = None
        if os.path.exists(local_version_path):
            try:
                with open(local_version_path, 'r', encoding='utf-8') as f:
                    local_version = f.read().strip()
            except Exception:
                pass
        need_update = (not os.path.exists(system_folder)) or (local_version != remote_system_version)
        if not need_update:
            self.status.setText("Cliente Actualizado")
            self.start_btn.setEnabled(True)
            self.set_start_btn_style(enabled=True, glow=True)
            return
        # Descargar y reemplazar system
        self.status.setText(f"Descargando System version {remote_system_version}")
        QtWidgets.QApplication.processEvents()
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, 'system.zip')
        try:
            r = requests.get(system_url, stream=True, timeout=60)
            r.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            self.status.setText('Error descargando el sistema.')
            return
        if os.path.exists(system_folder):
            try:
                shutil.rmtree(system_folder)
            except Exception as e:
                self.status.setText('Error eliminando carpeta system.')
                return
        try:
            self.status.setText('Descomprimiendo sistema...')
            # Verificar si el ZIP es válido antes de extraer
            import zipfile
            if not zipfile.is_zipfile(zip_path):
                self.status.setText('El archivo descargado no es un ZIP válido.\nVerifica la URL o tu conexión.')
                os.remove(zip_path)
                return
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                try:
                    zip_ref.extractall(system_folder, pwd=b'12345')
                except RuntimeError as e:
                    # Si falla por contraseña incorrecta o no cifrado, volver a intentar sin pwd
                    if 'password required' in str(e).lower() or 'bad password' in str(e).lower():
                        self.status.setText('Contraseña incorrecta para el ZIP del system.')
                        print('[ERROR][Descomprimiendo system] Contraseña incorrecta para el ZIP.')
                        return
                    else:
                        zip_ref.extractall(system_folder)

            self.status.setText(f"Sistema actualizado a v{remote_system_version}.")
            self.start_btn.setEnabled(True)
            self.set_start_btn_style(enabled=True, glow=True)
        except Exception as e:
            self.status.setText(f'Error descomprimiendo el sistema: {e}')
            print(f'[ERROR][Descomprimiendo system] {type(e).__name__}: {e}')
            if os.path.exists(zip_path):
                os.remove(zip_path)

    def init_ui(self):
        self.setStyleSheet('background-color: #181818;')
        # Banner superior
        self.banner = QtWidgets.QLabel(self)
        self.banner.setPixmap(QtGui.QPixmap(resource_path('assets/banner.png')).scaled(640, 80, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        self.banner.setGeometry(0, 0, 640, 80)
        self.banner.setAlignment(QtCore.Qt.AlignCenter)

        # Fondo principal debajo del banner
        self.bg = QtWidgets.QLabel(self)
        self.bg.setPixmap(QtGui.QPixmap(resource_path('assets/bg.png')).scaled(640, 340))
        self.bg.setGeometry(0, 80, 640, 340)
        self.bg.lower()

        # Botón de idioma (flag)
        self.lang_btn = QtWidgets.QPushButton(self)
        self.lang_btn.setIcon(QtGui.QIcon(resource_path('assets/flag.png')))
        self.lang_btn.setIconSize(QtCore.QSize(32, 32))
        self.lang_btn.setGeometry(590, 10, 32, 32)
        self.lang_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: rgba(255, 204, 102, 0.18);
                border-radius: 8px;
                border: 1px solid #ffcc66;
            }
        ''')
        self.lang_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lang_btn.clicked.connect(self.switch_language)

        # Botón iniciar
        self.start_btn = QtWidgets.QPushButton(LANGS[self.lang]['start'], self)
        self.start_btn.setGeometry(470, 340, 150, 50)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_game)
        self.start_btn.setGraphicsEffect(None)
        self.start_btn_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.start_btn_shadow.setBlurRadius(0)
        self.start_btn.setGraphicsEffect(self.start_btn_shadow)
        self.set_start_btn_style(enabled=False, glow=False)
        self.start_btn.show()
        self.bg.repaint()
        self.update()

        # Recuadro de noticias
        self.news_widget = QtWidgets.QWidget(self)
        self.news_widget.setGeometry(50, 90, 550, 240)
        self.news_widget.setStyleSheet('background-color: rgba(0,0,0,0.65); border-radius: 12px;')
        self.news_layout = QtWidgets.QVBoxLayout(self.news_widget)
        self.news_layout.setContentsMargins(16, 16, 16, 16)
        self.news_layout.setSpacing(8)
        # Cabecera con nombre del servidor
        self.news_header = QtWidgets.QLabel(self.config['LauncherTitle'], self.news_widget)
        self.news_header.setStyleSheet('color: #ffcc66; font-size: 20px; font-weight: bold;')
        self.news_layout.addWidget(self.news_header)
        # Área de noticias scrollable
        self.news_area = QtWidgets.QTextEdit(self.news_widget)
        self.news_area.setReadOnly(True)
        self.news_area.setStyleSheet('background: transparent; color: #fff; font-size: 15px; border: none;')
        self.news_layout.addWidget(self.news_area, stretch=1)
        # Estado centrado (más a la izquierda y alineado con el botón de jugar)
        self.status = QtWidgets.QLabel(LANGS[self.lang]['checking'], self)
        self.status.setGeometry(30, 350, 400, 30)
        self.status.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.status.setStyleSheet('color: #fff; font-size: 16px; background: rgba(0,0,0,0.5); font-weight: bold; border-radius: 6px; padding-left: 8px;')
        self.show()
        # Cargar noticias
        self.load_news()

    # check_integrity_with_manifest eliminada, ya no se usa

    def load_news(self):
        import requests
        import csv
        from io import StringIO
        news_url = self.config.get('NewsUrl', '').strip()
        lang_col = 0 if self.lang == 'es' else 1
        try:
            html = ''
            if news_url:
                resp = requests.get(news_url, timeout=5)
                if resp.status_code == 200:
                    resp.encoding = 'utf-8'
                    csvfile = StringIO(resp.text)
                    reader = csv.reader(csvfile)
                    rows = list(reader)
                    if rows and len(rows) > 1:
                        # Primera fila: cabecera, resto: noticias (solo filas válidas)
                        noticias = []
                        for r in rows[1:]:
                            if len(r) > lang_col and r[lang_col].strip():
                                noticias.append(r[lang_col].strip())
                        if noticias:
                            apertura = noticias[0]
                            html += f'<b>{apertura}</b><br><br>'
                            for noticia in reversed(noticias[1:]):
                                html += f'- {noticia}<br>'
                        else:
                            html += '<i>No hay novedades del servidor en este momento.</i>'
                    else:
                        html += '<i>No hay novedades del servidor en este momento.</i>'
                    self.news_area.setHtml(html)
                    return
        except Exception as e:
            self.news_area.setHtml('<i>No se pudo conectar para comprobar novedades.</i>')
            return

        self.news_area.setHtml('<i>No se pudo conectar para comprobar novedades.</i>')

    def switch_language(self):
        self.lang = 'en' if self.lang == 'es' else 'es'
        self.save_lang_setting(self.lang)
        self.update_ui_language()
        # Traducir status si es uno de los mensajes conocidos
        current_status = self.status.text().strip()
        for key in LANGS['es']:
            if current_status == LANGS['es'][key] or current_status == LANGS['en'][key]:
                self.status.setText(LANGS[self.lang][key])
                break
        # Traducción especial para "Cliente Actualizado" y "Descargando System version..."
        if current_status.startswith("Cliente Actualizado") or current_status.startswith("Client Updated"):
            self.status.setText("Cliente Actualizado" if self.lang=='es' else "Client Updated")
        elif current_status.startswith("Descargando System version") or current_status.startswith("Downloading System version"):
            import re
            m = re.match(r"Descargando System version ([^\.]+)(\.\.\.(\s*\d+%)?)?", current_status)
            if m:
                ver = m.group(1)
                percent = m.group(3) or ""
                msg = (f"Descargando System version {ver}... {percent}" if self.lang=='es' else f"Downloading System version {ver}... {percent}")
                self.status.setText(msg.strip())


    def update_ui_language(self):
        # Actualiza los textos de la UI al cambiar idioma
        self.start_btn.setText(LANGS[self.lang]['start'])
        # El status solo se actualiza si está en estado inicial o listo
        if self.status.text() in (LANGS['es']['checking'], LANGS['en']['checking']):
            self.status.setText(LANGS[self.lang]['checking'])
        elif self.status.text() in (LANGS['es']['ready'], LANGS['en']['ready']):
            self.status.setText(LANGS[self.lang]['ready'])
        # Recarga las noticias en el idioma correspondiente
        self.load_news()

    def load_lang_setting(self):
        import configparser
        settings = configparser.ConfigParser()
        settings_path = os.path.join('system', 'settings.ini')
        if os.path.exists(settings_path):
            settings.read(settings_path, encoding='utf-8')
            return settings.get('main', 'lang', fallback='es')
        return 'es'

    def save_lang_setting(self, lang):
        import configparser
        settings = configparser.ConfigParser()
        settings['main'] = {'lang': lang}
        settings_path = os.path.join('system', 'settings.ini')
        os.makedirs('system', exist_ok=True)
        with open(settings_path, 'w', encoding='utf-8') as f:
            settings.write(f)

    def start_game(self):
        import subprocess
        import os
        exe = self.config.get('StartFile')
        if not exe:
            msg = ("Error: No se ha configurado el ejecutable (StartFile) en launcher.json" if self.lang == 'es' else "Error: The executable (StartFile) is not configured in launcher.json")
            self.status.setText(msg)
            return
        exe_path = os.path.join(os.getcwd(), 'system', exe)
        if not os.path.isfile(exe_path):
            msg = (f"Error: No se encontró el ejecutable: {exe}" if self.lang == 'es' else f"Error: Executable not found: {exe}")
            self.status.setText(msg)
            return
        try:
            os.startfile(exe_path)
            QtCore.QCoreApplication.quit()
        except Exception as e:
            msg = (f"Error al iniciar el juego: {e}" if self.lang == 'es' else f"Error launching the game: {e}")
            self.status.setText(msg)

    def set_start_btn_style(self, enabled, glow):
        if not enabled:
            self.start_btn.setStyleSheet('''
                QPushButton {
                    background-color: #444;
                    color: #888;
                    font-size: 22px;
                    border-radius: 8px;
                    border: 2px solid #ffcc66;
                }
            ''')
            self.start_btn.setGraphicsEffect(None)  # Elimina sombra
        elif glow:
            self.start_btn.setStyleSheet('''
                QPushButton {
                    background-color: #222;
                    color: #fff;
                    font-size: 22px;
                    border-radius: 8px;
                    border: 2px solid #ffcc66;
                    outline: 0;
                }
                QPushButton:hover {
                    background-color: #2a2a00;
                    color: #fffbe0;
                    border: 2px solid #ffe066;
                }
            ''')
            # Crea un nuevo efecto cada vez para evitar errores de objeto eliminado
            shadow = QtWidgets.QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(32)
            shadow.setColor(QtGui.QColor(255, 204, 102, 180))
            shadow.setOffset(0, 0)
            self.start_btn.setGraphicsEffect(shadow)  # Aplica sombra
        else:
            self.start_btn.setStyleSheet('''
                QPushButton {
                    background-color: #222;
                    color: #fff;
                    font-size: 22px;
                    border-radius: 8px;
                    border: 2px solid #ffcc66;
                }
                QPushButton:hover {
                    background-color: #333;
                    color: #fff;
                }
            ''')
            self.start_btn.setGraphicsEffect(None)  # Elimina sombra


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec_())
