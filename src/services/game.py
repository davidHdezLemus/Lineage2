import os
import subprocess
from typing import Dict, Callable

class GameService:
    def __init__(self, config: Dict, status_callback: Callable):
        """
        Manages launching the game executable.
        :param config: The application configuration dictionary.
        :param status_callback: A function to report status messages to the UI.
        """
        self.config = config
        self.status_callback = status_callback

    def start(self):
        """
        Validates the game executable path and launches the game.
        Reports errors via the status callback.
        """
        exe_name = self.config.get('StartFile')
        if not exe_name:
            self.status_callback("Error: No se ha configurado el ejecutable (StartFile).", error=True)
            return False

        exe_path = os.path.join(os.getcwd(), 'system', exe_name)
        if not os.path.isfile(exe_path):
            self.status_callback(f"Error: No se encontró el ejecutable: {exe_name}", error=True)
            return False

        try:
            os.startfile(exe_path)
            return True
        except Exception as e:
            self.status_callback(f"Error al iniciar el juego: {e}", error=True)
            return False