from src.infrastructure.database.postgresql import Postgresql
from src.infrastructure.database.postgresql.utils import get_db_cursor


class PersonDAOTest:
    def __init__(self, db: Postgresql):
        self.db = db

    def get_basic_info(self):
        with get_db_cursor(self.db) as cursor:
            cursor.execute("SELECT * FROM person;")
            results = cursor.fetchall()
            return results
