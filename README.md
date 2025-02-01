# G3_BackEndPython

API desarrollada en **FastAPI** para permitir el registro de planes de prevención y descontaminación ambiental, así como el registro de reportes de las medidas requeridas por los organismos sectoriales.

## 📌 Requisitos previos
Antes de comenzar, asegúrate de tener instalado:

- **Python** (ver versión requerida en `pyproject.toml`)
- **Poetry** (gestor de dependencias)
- **Uvicorn** (para ejecutar el servidor)
- **PostgreSQL 17.2.3** (base de datos)

## ⚙ Instalación de Poetry
### En macOS:
```sh
brew install pipx
pipx install poetry
```

### En Windows:
```sh
py -m pip install pipx
pipx install poetry==1.8.5
```

## 📦 Instalación de dependencias
Ejecuta el siguiente comando en la raíz del proyecto:
```sh
poetry install
```

⚠ **Nota**: Si hay problemas con la versión de Python detectada por Poetry, usa:
```sh
poetry env use path/to/python.exe
```
Luego, vuelve a instalar las dependencias con `poetry install`.

## 🚀 Ejecutar el proyecto
### Activar el entorno virtual
Si la versión de Poetry instalada tiene el comando `shell`, usa:
```sh
poetry shell
```
Si no está disponible, activa manualmente el entorno virtual con:
```sh
source .venv/bin/activate  # En macOS/Linux
.venv\Scripts\activate     # En Windows
```

### Iniciar el servidor
```sh
uvicorn main:app --reload
```

## 🔄 Manejo de dependencias
Si alguien hace un push con nuevas dependencias y necesitas actualizarlas, ejecuta:
```sh
poetry lock
poetry install
```

## ⚙ Configuración del entorno
Si el archivo `.env` no existe en el directorio del proyecto, créalo con el siguiente contenido:
```ini
APP_TIMEZONE_LOCAL=America/Santiago
DB_DBNAME=
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```
**Nota:** Asegúrate de modificar los valores según la configuración de tu base de datos.

## 🗂 Base de Datos
La aplicación utiliza **PostgreSQL 17.2.3** como base de datos.

A continuación, se presentan los diagramas de entidad-relación con los modelos planteados:

##### Diagrama Entidad Relación: PLAN
![Diagrama Entidad-Relación: PLAN](./docs/database/erd/PLAN.erd.png)

##### Diagrama Entidad Relación: REPORTE
![Diagrama Entidad-Relación: REPORTE](./docs/database/erd/REPORTE.erd.png)

##### Diagrama Entidad Relación: USUARIO
![Diagrama Entidad-Relación: USUARIO](./docs/database/erd/USUARIO.erd.png)

Para el correcto funcionamiento de la aplicación, se debe montar el siguiente **backup** en la base de datos:

[Descargar Backup](./docs/database/backup/dump-PPDA-202501312151.sql)

⚠ **Nota:** Es necesario restaurar este backup antes de ejecutar la aplicación para garantizar la disponibilidad de los modelos requeridos.

