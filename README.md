# Lineage 2 - Modern Python Launcher

Un lanzador de juegos moderno y auto-actualizable para Lineage 2, construido con Python y PyQt5. Este proyecto proporciona una base sólida y fácil de mantener para lanzar y actualizar un cliente de juego, con una arquitectura modular y limpia.

![Launcher Screenshot](src/assets/banner.png)

---

## ✨ Características

- **Auto-Actualización**: El lanzador comprueba si hay nuevas versiones de sí mismo y de los archivos del sistema del juego.
- **Interfaz Gráfica Moderna**: Interfaz de usuario limpia y atractiva construida con PyQt5.
- **Noticias del Servidor**: Muestra las últimas noticias cargadas desde una hoja de cálculo de Google.
- **Soporte Multi-idioma**: Fácilmente extensible para soportar múltiples idiomas (actualmente Español e Inglés).
- **Arquitectura Modular**: El código está separado en servicios (actualizaciones, noticias, idioma, juego) y UI, lo que facilita su mantenimiento y expansión.
- **Empaquetado Sencillo**: Incluye un archivo `.spec` para PyInstaller que facilita la creación de un ejecutable `.exe` de un solo archivo.

---

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura limpia para separar las responsabilidades:

- **`src/`**: Contiene todo el código fuente de la aplicación.
  - **`main.py`**: El punto de entrada de la aplicación. Orquesta la UI y los servicios.
  - **`config/`**: Contiene la configuración estática de la aplicación (`config.py`).
  - **`core/`**: Lógica de bajo nivel, como el `SystemManager` para interactuar con los archivos del juego.
  - **`services/`**: Lógica de negocio (actualizador, noticias, idioma, lanzamiento del juego).
  - **`ui/`**: Define la interfaz de usuario (`launcher_ui.py`).
  - **`utils/`**: Utilidades compartidas, como el manejo de `resource_path`.
  - **`assets/`**: Todos los recursos gráficos (imágenes, iconos).
- **`package.spec`**: Archivo de configuración para PyInstaller para construir el ejecutable.
- **`requirements.txt`**: Lista de dependencias de Python.

---

## 🚀 Instalación y Uso

### 1. Prerrequisitos

- Python 3.8 o superior.
- `pip` para instalar paquetes.

### 2. Instalación de Dependencias

Clona el repositorio y navega hasta el directorio del proyecto. Luego, instala las dependencias:

```sh
pip install -r requirements.txt
```

### 3. Configuración

Edita el archivo `src/config/config.py` para ajustar los parámetros del lanzador:

```python
# src/config/config.py
CONFIG = {
    "LauncherVersion": "1.2", # Cambia esto para forzar una actualización del lanzador
    "LauncherTitle": "Lineage 2 - CT-0 High Five",
    "NewsUrl": "https://docs.google.com/spreadsheets/d/e/2PACX-1v.../pub?output=csv",
    "VersionJsonUrl": "https://github.com/user/repo/raw/main/version.json",
    "StartFile": "l2.exe"
}
```

Asegúrate de que tu `VersionJsonUrl` apunte a un archivo `version.json` con la siguiente estructura:

```json
{
  "launcher": {
    "version": "1.2",
    "url": "https://github.com/user/repo/raw/main/dist/Lineage2_Launcher.exe"
  },
  "system": {
    "version": "1.0.2",
    "url": "https://github.com/user/repo/raw/main/system.zip"
  }
}
```

### 4. Ejecutar en Modo Desarrollo

Para probar el lanzador sin compilarlo, ejecuta:

```sh
python src/main.py
```

---

## 📦 Compilar el Ejecutable

Para crear un único archivo `.exe` para distribución, usa PyInstaller con el archivo `.spec` proporcionado.

1.  **Instala PyInstaller:**
    ```sh
    pip install pyinstaller
    ```

2.  **Ejecuta PyInstaller:**
    ```sh
    pyinstaller package.spec
    ```

3.  **Encuentra tu ejecutable:**
    El archivo `Lineage2_Launcher.exe` estará en la carpeta `dist/`. ¡Listo para distribuir!

---

## 🤝 Cómo Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar este lanzador, por favor sigue estos pasos:

1.  **Haz un Fork** del repositorio.
2.  **Crea una nueva rama** para tu característica (`git checkout -b feature/nueva-caracteristica`).
3.  **Haz tus cambios** y haz commit (`git commit -am 'Añade nueva característica'`).
4.  **Sube tus cambios** a tu fork (`git push origin feature/nueva-caracteristica`).
5.  **Abre un Pull Request**.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Desarrollado por

-   **David Hdez Lemus** y colaboradores.
