from psycopg2 import pool


class PostgresqlDB:
    def __init__(
        self, host, database, user, password, port, minconn=1, maxconn=10
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        try:
            self._pool = pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host=host,
                database=database,
                user=user,
                password=password,
                port=port,
            )

            if self._pool:
                print("Pool of connections was initialized successfully.")
        except Exception as e:
            print("Error initializing connection pool: ", e)
            raise e

    def get_connection(self):
        try:
            return self._pool.getconn()
        except Exception as e:
            print("Error getting connection: ", e)
            raise e

    def put_connection(self, conn):
        try:
            self._pool.putconn(conn)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Error returning connection: ", e)

    def close_all_connections(self):
        try:
            self._pool.closeall()
            print("All connections were closed successfully")
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Error closing all connections: ", e)
