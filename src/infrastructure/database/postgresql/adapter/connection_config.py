from dotenv import load_dotenv

from src.infrastructure.database.postgresql.postgresql import Postgresql
from src.util import (
    Enviroments,
    decode_base64_password,
)


load_dotenv()


def create_database_connection():
    config = {
        "host": Enviroments.DB_HOST,
        "database": Enviroments.DB_NAME,
        "user": Enviroments.DB_USER,
        "port": Enviroments.DB_PORT,
        "password": decode_base64_password(Enviroments.DB_PASSWORD_BASE64),
    }
    db_connection_instance = Postgresql(**config)

    return db_connection_instance
