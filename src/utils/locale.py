import os
import configparser

# Dictionary with all the application's localizable strings
LANGS = {
    'es': {
        'start': 'JUGAR',
        'checking': 'Comprobando actualizaciones...',
        'updating': 'Actualizando archivos...',
        'ready': 'Listo para jugar',
        'update_failed': 'No se pudo conectar con el servidor de actualizaciones.',
        'client_updated': 'Cliente Actualizado',
        'downloading_system': 'Descargando System version'
    },
    'en': {
        'start': 'PLAY',
        'checking': 'Checking updates...',
        'updating': 'Updating files...',
        'ready': 'Ready to play',
        'update_failed': 'Could not connect to the update server.',
        'client_updated': 'Client Updated',
        'downloading_system': 'Downloading System version'
    }
}

class LocaleService:
    def __init__(self, settings_dir: str = 'system'):
        """
        Manages loading and saving language settings.
        :param settings_dir: The directory where the settings.ini file is stored.
        """
        self.settings_path = os.path.join(settings_dir, 'settings.ini')
        self.settings_dir = settings_dir

    def get_language(self) -> str:
        """
        Loads the language from settings.ini, defaulting to 'es'.
        """
        if not os.path.exists(self.settings_path):
            return 'es'
        
        config = configparser.ConfigParser()
        try:
            config.read(self.settings_path, encoding='utf-8')
            return config.get('main', 'lang', fallback='es')
        except (configparser.Error, IOError):
            return 'es'

    def save_language(self, lang: str):
        """
        Saves the selected language to settings.ini.
        """
        config = configparser.ConfigParser()
        config['main'] = {'lang': lang}
        
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                config.write(f)
        except IOError as e:
            print(f"Error saving language setting: {e}")