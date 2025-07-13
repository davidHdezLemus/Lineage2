# Lineage 2 Launcher - CT-0 High Five

Este launcher gestiona la actualización y el inicio del cliente Lineage 2 de forma automática y sencilla, con soporte multi-idioma (español/inglés) y mensajes de estado claros para el usuario.

---

## Contenido del proyecto

- `launcher.py` — Script principal del launcher (PyQt5). **Debe estar presente tanto para desarrollo como para el empaquetado con PyInstaller.**
- `launcher.json` — Configuración del launcher (título, URLs, ejecutable, versión local, URL del version.json remoto).

Ejemplo de `launcher.json`:
```json
{
  "LauncherTitle": "Lineage 2 - CT-0 High Five",
  "NewsUrl": "https://tu-url-de-noticias.com/noticias.csv",
  "LauncherVersion": "1.1",
  "VersionJsonUrl": "https://tu-url.com/version.json",
  "StartFile": "l2.exe"
}
```

El archivo `version.json` remoto (en GitHub) debe tener la siguiente estructura:
```json
{
  "launcher": {
    "version": "1.1",
    "url": "https://tu-url.com/launcher.exe"
  },
  "system": {
    "version": "1.0.1",
    "url": "https://tu-url.com/system.zip"
    "url": "https://github.com/davidHdezLemus/Lineage2/raw/refs/heads/main/system.zip"
  }
}
```

- `requirements.txt` — Dependencias Python necesarias.
- Carpeta `assets/` — Recursos gráficos (icono, imágenes, etc).
- **NO incluir** `settings.ini` en el bundle: este archivo se genera automáticamente en `system/` al cambiar el idioma.

---

## Instalación, desarrollo y empaquetado

1. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Modo desarrollo:**
   - Ejecuta `python launcher.py` para probar el launcher sin empaquetar.
   - Si hay una actualización del launcher, el nuevo `.exe` se descargará en la carpeta `temp/` del proyecto y **no se reemplazará nada automáticamente**.
   - Se mostrará un mensaje con la ruta del archivo descargado para pruebas manuales.

3. **Empaqueta el launcher en un solo ejecutable (comando directo):**
   ```sh
   pyinstaller --onefile --noconsole --icon=assets/icon.ico --add-data "assets;assets" --add-data "launcher.json;." --add-data "requirements.txt;." launcher.py
   ```
   - El ejecutable aparecerá en la carpeta `dist/`.
   - Copia (si existe) tu archivo `settings.ini` junto al `.exe` para conservar la configuración de idioma.

---

### Empaquetado avanzado usando `launcher.spec`

Si prefieres mayor control o personalización, puedes empaquetar usando el archivo `launcher.spec` incluido en el proyecto. Este archivo ya incluye la configuración para añadir la carpeta `assets/`, el `launcher.json`, el `requirements.txt` y el icono.

1. Asegúrate de tener las dependencias instaladas:
   ```sh
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Empaqueta usando el archivo `.spec`:
   ```sh
   pyinstaller launcher.spec
   ```

   - El ejecutable aparecerá en la carpeta `dist/` con todos los recursos necesarios.
   - Puedes editar el `.spec` si necesitas añadir más archivos o cambiar el nombre del ejecutable.

> **Nota:** Usar el `.spec` es equivalente a pasar los argumentos manualmente, pero es más flexible para proyectos grandes o si necesitas personalizar la distribución.

4. **Modo producción (usuario final):**
   - Ejecuta `Launcher.exe`.
   - Si hay una actualización del launcher, el `.exe` se descargará y el reemplazo será automático mediante un script `.bat`.

5. **Estructura de distribución recomendada:**
   ```
   dist/
     ├─ Launcher.exe
     ├─ launcher.py        # (solo necesario para desarrollo o recompilación)
     ├─ launcher.json
     ├─ requirements.txt
     ├─ assets/
     │    └─ icon.ico, ...
     └─ settings.ini  (opcional, generado tras primer uso)
   ```

---

## Flujo de actualización automática

- El launcher lee la versión local y la URL del archivo remoto desde `launcher.json`.
- Descarga el `version.json` remoto y compara versiones:
  - Si hay una versión nueva del launcher:
    - **Modo developer:** descarga el `.exe` en `./temp/` y muestra la ruta.
    - **Modo producción:** descarga el `.exe` y ejecuta un `.bat` para reemplazar el actual automáticamente.
  - Si hay una nueva versión del system, descarga y reemplaza la carpeta `system/`.

---

## Personalización y configuración

- Edita `launcher.json` para cambiar URLs, título, versión local, URL de actualizaciones o el ejecutable a lanzar.
- El archivo `settings.ini` almacena solo la preferencia de idioma y se puede borrar para restablecer.
- Puedes personalizar el icono cambiando `assets/icon.ico` y recompilando.

---

## Notas técnicas

- El launcher es compatible con Windows y empaquetado con PyInstaller.
- Todos los recursos se acceden correctamente tanto en desarrollo como en ejecutable gracias a la función `resource_path`.
- El archivo `settings.ini` **no debe incluirse** en el bundle para que el usuario conserve su configuración entre versiones.
- Si ves errores de permisos al iniciar el juego, marca el ejecutable como "Ejecutar como administrador".

---

## Créditos

Desarrollado por David Hdez Lemus y colaboradores. Basado en PyQt5 y Python 3.8+.

---

¿Dudas o sugerencias? Abre un issue en el repositorio o contacta al desarrollador.
