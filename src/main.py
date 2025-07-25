import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, QtSvg
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QSplashScreen, QApplication

# Función auxiliar para obtener rutas de recursos
def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configuración inicial de la aplicación
app = QApplication(sys.argv)

# Crear y mostrar el splash screen
def show_splash():
    try:
        splash_pix = QtGui.QPixmap(resource_path('assets/loading.png'))
        if splash_pix.isNull():
            # Si no se puede cargar la imagen, crear un splash screen simple
            splash = QSplashScreen(Qt.white)
            splash.showMessage(
                "Cargando...", 
                Qt.AlignBottom | Qt.AlignHCenter, 
                Qt.black
            )
        else:
            splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
            splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            splash.setEnabled(False)
            splash.showMessage(
                "Cargando...", 
                Qt.AlignBottom | Qt.AlignHCenter, 
                Qt.white
            )
        
        splash.show()
        app.processEvents()
        return splash
    except Exception as e:
        print(f"Error mostrando splash screen: {str(e)}")
        # Retornar None si hay algún error
        return None

# Mostrar el splash screen lo antes posible
splash = show_splash()

# Importaciones pesadas después de mostrar el splash
from core.updater import Updater
from config.config import CONFIG
from services.news import NewsService
from services.game import GameService
from utils.locale import LocaleService, LANGS
from ui.launcher_ui import LauncherUI

class Launcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.locale_service = LocaleService()
        self.lang = self.locale_service.get_language()
        
        self.setWindowTitle(self.config['LauncherTitle'])
        self.setFixedSize(640, 420)
        self.setWindowIcon(QtGui.QIcon(resource_path('assets/icon.png')))
        
        # Setup UI from the dedicated UI class
        self.ui = LauncherUI()
        self.ui.setup_ui(self)
        
        # Load news and start update check
        self.load_news()
        QtCore.QTimer.singleShot(500, self.check_updates)

    def log(self, message: str, error: bool = False):
        """Logs a message to the console and the UI status label."""
        prefix = "[ERROR]" if error else "[INFO]"
        print(f"{prefix} {message}")
        self.status.setText(message)
        QtWidgets.QApplication.processEvents()

    def load_config(self):
        """Loads configuration from config.py"""
        return CONFIG

    def check_updates(self):
        """Checks for updates using the Updater service."""
        updater = Updater(self.config)
        try:
            update_performed = updater.check_updates(self.log)
            
            if update_performed:
                self.log("Cliente actualizado con éxito.")
            else:
                self.log("No se encontraron actualizaciones. El cliente ya está al día.")

            # Enable the start button once checks are complete
            self.start_btn.setEnabled(True)
            self.ui.set_start_btn_style(self.start_btn, enabled=True, glow=True)
            self.status.setText(LANGS[self.lang]['ready'])

        except Exception as e:
            self.log(f"Error fatal en el proceso de actualización: {e}", error=True)
            self.status.setText(LANGS[self.lang]['update_failed'])

    def load_news(self):
        """Loads news by using the NewsService."""
        news_service = NewsService(self.config, self.lang)
        news_html = news_service.get_news_html()
        self.news_area.setHtml(news_html)

    def switch_language(self):
        """Switches the UI language and saves the setting."""
        self.lang = 'en' if self.lang == 'es' else 'es'
        self.locale_service.save_language(self.lang)
        self.update_ui_language()
        
        current_status = self.status.text().strip()
        # Translate known status messages
        for key, value in LANGS['es'].items():
            if current_status == value:
                self.status.setText(LANGS[self.lang][key])
                return
        for key, value in LANGS['en'].items():
            if current_status == value:
                self.status.setText(LANGS[self.lang][key])
                return

        # Special translation for dynamic messages
        if LANGS['es']['client_updated'] in current_status or LANGS['en']['client_updated'] in current_status:
            self.status.setText(LANGS[self.lang]['client_updated'])
        elif LANGS['es']['downloading_system'] in current_status or LANGS['en']['downloading_system'] in current_status:
            import re
            match = re.search(r'(\d+(\.\d+)?)', current_status)
            version = match.group(1) if match else ''
            self.status.setText(f"{LANGS[self.lang]['downloading_system']} {version}...")

    def update_ui_language(self):
        """Updates all localizable UI elements to the current language."""
        self.start_btn.setText(LANGS[self.lang]['start'])
        
        if self.status.text() in (LANGS['es']['checking'], LANGS['en']['checking']):
            self.status.setText(LANGS[self.lang]['checking'])
        elif self.status.text() in (LANGS['es']['ready'], LANGS['en']['ready']):
            self.status.setText(LANGS[self.lang]['ready'])
            
        self.load_news()

    def start_game(self):
        """Initializes GameService and starts the game."""
        game_service = GameService(self.config, self.log)
        if game_service.start():
            QtCore.QCoreApplication.quit()


if __name__ == '__main__':
    try:
        launcher = Launcher()
        launcher.show()
        # Cerrar el splash screen cuando la ventana principal esté lista
        if splash is not None:
            splash.finish(launcher)
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
        if splash is not None:
            splash.close()
        sys.exit(1)
