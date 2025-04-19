import json
import pathlib
import bcrypt
import pytz
from datetime import datetime, timedelta, timezone
from fastapi.openapi.models import Example
from jose import jwt

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, APP_TIMEZONE_LOCAL, REFRESH_TOKEN_EXPIRE_DAYS, TOKEN_ALGORITHM, TOKEN_SECRET_KEY


def get_local_now_datetime() -> datetime:
    """
    Devuelve la fecha y hora actuales en la zona horaria local (APP_TIMEZONE_LOCAL).
    :return: La fecha y hora actuales en la zona horaria local.
    """
    local_tz = pytz.timezone(APP_TIMEZONE_LOCAL)
    return datetime.now(local_tz)

def get_example(filename: str) -> Example:
    """
    Lee un archivo JSON con nombre especificado en la ruta ./examples/
    y devuelve su contenido como un objeto Example de FastAPI.

    :param filename: Nombre del archivo JSON a leer.
    :return: El contenido del archivo en formato Example de FastAPI.
    :raises FileNotFoundError: Si el archivo no existe.
    """
    api_examples_path = pathlib.Path(__file__).parent.parent.parent / "api" / "examples"
    filepath = api_examples_path / f"{filename}.json"
    if filepath.exists():
        with open(filepath) as f:
            return Example(value=json.load(f))
    
example_data = {}

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Genera un token de acceso con los datos especificados y una fecha de expiración.
    
    :param data: Diccionario con los datos a incluir en el token.
    :param expires_delta: Opcional. Tiempo de expiración del token. Si no se especifica, se utiliza el valor en ACCESS_TOKEN_EXPIRE_MINUTES.
    :return: El token de acceso.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)

def create_refresh_token(data: dict):
    """
    Genera un token de refresh con los datos especificados y una fecha de expiración en días segun el valor en REFRESH_TOKEN_EXPIRE_DAYS.
    
    :param data: Diccionario con los datos a incluir en el token.
    :return: El token de refresh.
    """
    new_data = data.copy()
    new_data.update({"type": "refresh"})
    return create_access_token(new_data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def verify_password(plain_password, hashed_password):
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada con bcrypt.
    
    :param plain_password: La contraseña en texto plano a verificar.
    :param hashed_password: La contraseña hasheada con bcrypt a verificar.
    :return: True si coincide, False en caso contrario.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    """
    Crea un hash para una contrase a en texto plano utilizando bcrypt.
    
    :param password: La contrase a en texto plano a hashear.
    :return: El hash de la contraseña.
    """
    pwd_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=bcrypt.gensalt())
    return hashed_password.decode('utf-8')