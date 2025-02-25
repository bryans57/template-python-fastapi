from src.infrastructure.database.postgresql import PostgresqlDB
from src.infrastructure.database.postgresql.utils import get_db_cursor


class PersonDAOTest:
    def __init__(self, db: PostgresqlDB):
        self.db = db

    def get_basic_info(self):
        with get_db_cursor(self.db) as cursor:
            cursor.execute("SELECT * FROM person;")
            results = cursor.fetchall()
            return results

    def get_person_info(self, identification):
        query = "SELECT * FROM person WHERE identification = %s"
        with get_db_cursor(self.db) as cursor:
            cursor.execute(query, (identification,))
            return cursor.fetchall()
