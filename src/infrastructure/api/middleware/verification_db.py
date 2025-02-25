from contextlib import asynccontextmanager

from fastapi import FastAPI
from psycopg2 import OperationalError

from src.conf import injector
from src.domain.exceptions import DatabaseErrorHandling
from src.infrastructure.database.postgresql.postgresqldb import PostgresqlDB


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    """
    print("Starting application...")

    try:
        db_instance = injector.get(PostgresqlDB)
        conn = db_instance.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            print("Initial database connection verified.")
        db_instance.put_connection(conn)
    except OperationalError as e:
        raise DatabaseErrorHandling(e) from e
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("Don't track error: ", e)
        raise e
    yield
    print("Turn down the app...")
    try:
        db_instance.close_all_connections()
        print("Database connections closed.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("Error at close connections", e)
