from typing import List

from injector import inject
from psycopg2 import (
    DatabaseError,
    sql,
)
from psycopg2.extras import RealDictCursor

from src.domain.exceptions import DatabaseErrorHandling
from src.domain.models import Person
from src.domain.repositories import PersonRepository
from src.infrastructure.database.postgresql.postgresql import Postgresql


class PersonDAO(PersonRepository):
    @inject
    def __init__(self, db: Postgresql):
        self.db = db

    def get_info(self, identifications: list, fields_info: list) -> List[Person]:
        con = self.db.get_connection()
        try:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                filtered_fields_info = [field for field in fields_info if field != "identification"]
                fields_set = sql.SQL(", ").join(map(sql.Identifier, filtered_fields_info))
                query = sql.SQL(
                    """
						WITH list_person AS (
                            SELECT DISTINCT UNNEST(ARRAY [%s]) AS identification
                        )
                        SELECT lp.identification, {fields}
                        FROM list_person lp
                        LEFT JOIN person p ON lp.identification = p.identification;
					"""
                ).format(fields=fields_set)
                cursor.execute(query, (identifications,))
                results = cursor.fetchall()
                result_convert = [Person(**fila) for fila in results]
                return result_convert
        except DatabaseError as e:
            raise DatabaseErrorHandling(e) from e
        finally:
            self.db.put_connection(con)
