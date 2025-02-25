from src.infrastructure.database.postgresql import PostgresqlDB
from src.infrastructure.database.postgresql.utils import get_db_cursor


class GenericDAOTest:
    def __init__(self, db: PostgresqlDB):
        self.db = db

    def execute_query(self, query: str):
        with get_db_cursor(self.db) as cursor:
            cursor.execute(query)

            # Check if query is a SELECT statement before fetching results
            if query.strip().upper().startswith("SELECT"):
                if cursor.rowcount == 1:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
            else:
                result = cursor.rowcount  # Return affected rows for non-SELECT queries

        return result
