import os
import sys

from dotenv import load_dotenv


load_dotenv()


class Enviroments:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD_BASE64 = os.getenv("DB_PASSWORD_BASE64")
    DB_PORT = os.getenv("DB_PORT")
    ENV = os.getenv("ENV")
    APP_NAME = os.getenv("APP_NAME")
    DOMAIN = os.getenv("DOMAIN")
    URL_SERVICE = os.getenv("URL_SERVICE")
    PREFIX = ""
    PYTEST = os.getenv("PYTEST")

    @staticmethod
    def validate():
        missing_vars = [
            var
            for var in [
                "DB_HOST",
                "DB_NAME",
                "DB_USER",
                "DB_PASSWORD_BASE64",
                "DB_PORT",
                "ENV",
                "APP_NAME",
                "DOMAIN",
                "URL_SERVICE",
            ]
            if os.getenv(var) is None
        ]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")


Enviroments.PYTEST = "pytest" in sys.modules

# Validacion de dependencias
Enviroments.validate()

Enviroments.PREFIX = f"/{Enviroments.DOMAIN}/{Enviroments.URL_SERVICE}"
