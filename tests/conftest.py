from unittest.mock import patch

import psycopg2
import pytest

from psycopg2.extensions import connection
from pytest_postgresql import factories

from src.conf import injector
from src.infrastructure.database.postgresql import Postgresql
from tests.config.mocks.tablas import TestDB


def load_basic_database(**kwargs):
    db_connection: connection = psycopg2.connect(**kwargs)
    try:
        with db_connection.cursor() as cur:

            # Create tables
            for identificador in TestDB:
                try:
                    cur.execute(identificador.value)
                    print(f"Executed: {identificador}")
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Error executing {identificador}: {e}")
                    db_connection.rollback()  # Rollback on failure
                    continue  # Move to the next SQL statement

            # Load base data like master tables
            try:
                # You can load here if you a master like a table of cities
                db_connection.commit()
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Error during test data load: {e}")
                db_connection.rollback()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error carga inicial: {e}")
    finally:
        db_connection.close()


# Define the PostgreSQL process factory with the schema loading function
postgresql_proc = factories.postgresql_proc(
    load=[load_basic_database],
)

# Define a PostgreSQL client fixture that depends on the process fixture
postgresql = factories.postgresql("postgresql_proc")  # pylint: disable=redefined-outer-name


@pytest.fixture(scope="function")
def postgresql_instance(postgresql):  # pylint: disable=redefined-outer-name
    # Initialize the Postgresql connection pool once for the entire session
    test_db = Postgresql(
        host=postgresql.info.host,
        database=postgresql.info.dbname,
        user=postgresql.info.user,
        password=postgresql.info.password,
        port=postgresql.info.port,
    )
    yield test_db
    # Close all connections at the end of the session
    test_db.close_all_connections()


@pytest.fixture(scope="function")
def setup_db(postgresql_instance):  # pylint: disable=redefined-outer-name
    with patch(
        "src.infrastructure.database.postgresql.adapter.connection_config.create_database_connection",
        return_value=postgresql_instance,
    ):
        injector.binder.bind(Postgresql, to=postgresql_instance, scope=None)
        yield postgresql_instance
