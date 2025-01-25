# G3_BackEndPython

## Instalacion de gestor de paquetes [Poetry](https://python-poetry.org/)
Para instalar en `MAC` ejecutar los siguientes comandos
```sh
brew install pipx
pipx install poetry
```

Para instalar en `Windows` ejecutar los siguientes comandos
```sh
py -m pip install pipx
pipx install poetry==1.8.5
```

Una vez instalado Poetry, ejecutar el siguiente comando para instalar las dependencias del proyecto
```sh
poetry install
```

> [!WARNING]
> En caso de presentar algun conflicto con la version de python que detecta poetry se deberá ejecutar el comando `poetry env use path/to/python.exe` la version de python requerida se puede ver en el archivo `pyproject.toml`
> Una vez solucionada la versión de python, volver a ejecutar la instalación de dependencias.

# Ejecutar poetry
poetry install

# Volver a guardar librerias
Si alguien hace un push y no tiene las nuevas librerias puede ejecutar estos comandos
``sh
poetry lock
poetry install
```

# Ejecutar proyecto
Si la versión de Poetry instalada tiene el comando shell se deberá ejecutar para activar el ambiente virtual de python y poder acceder a los paquetes instalados como uvicorn
```sh
poetry shell
```
En caso de no disponer de este comando ejecutar normalmente con 
 ```sh
.venv/Script/activate 
```

finalmente iniciar el proyecto ejecutando el siguiente comando
```sh
uvicorn main:app --reload
```

# Parametrizaciones el ambiente de trabajo
En caso de no existir en el directorio del proyecto el archivo .env, se debe crear con el siguiente contenido:
```
APP_TIMEZONE_LOCAL=America/Santiago
DB_DBNAME=
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```
Se debe cambiar los valores por los correspondientes a la base de datos.
