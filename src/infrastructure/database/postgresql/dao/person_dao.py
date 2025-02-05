from contextlib import contextmanager
from typing import (
    List,
    Optional,
)

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

    @contextmanager
    def get_cursor(self):
        """Context manager to handle database connections safely."""
        con = self.db.get_connection()
        try:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
                con.commit()
        except DatabaseError as e:
            con.rollback()
            raise DatabaseErrorHandling(e) from e
        finally:
            self.db.put_connection(con)

    def get_info(self, identifications: list, fields_info: list) -> List[Person]:
        filtered_fields_info = [field for field in fields_info if field != "identification"]

        with self.get_cursor() as cursor:
            query = sql.SQL(
                """
                    WITH list_person AS (
                        SELECT DISTINCT UNNEST(ARRAY [%s]) AS identification
                    )
                    SELECT lp.identification, {fields}
                    FROM list_person lp
                    LEFT JOIN person p ON lp.identification = p.identification;
                """
            ).format(fields=sql.SQL(", ").join(map(sql.Identifier, filtered_fields_info)))

            cursor.execute(query, (identifications,))
            results = cursor.fetchall()

            return [Person(**fila) for fila in results]

    def add(self, person: Person) -> Person:
        # Convert person to a dictionary
        person_data = person.model_dump()
        fields, values = list(person_data.keys()), list(person_data.values())

        with self.get_cursor() as cursor:
            # Create SQL for fields and placeholders

            query = sql.SQL(
                """
                INSERT INTO person ({fields})
                VALUES ({placeholders})
                RETURNING *;
                """
            ).format(
                fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
                placeholders=sql.SQL(", ").join(sql.Placeholder() for _ in fields),
            )

            # Execute query with values
            cursor.execute(query, values)
            result = cursor.fetchone()
            return Person(**result)

    def update(self, person: Person) -> Person:
        # Convert person to a dictionary
        person_data = person.model_dump()
        filtered_person_data = {k: v for k, v in person_data.items() if k != "identification" and v is not None}

        with self.get_cursor() as cursor:
            fields = sql.SQL(", ").join(
                sql.Composed([sql.Identifier(field), sql.SQL(" = "), sql.Placeholder(f"{field}")])
                for field in filtered_person_data.keys()
            )

            query = sql.SQL(
                """
                UPDATE person
                SET {fields}
                WHERE identification = %(identification)s
                RETURNING *;
                """
            ).format(fields=fields)

            # Execute query with values
            cursor.execute(query, person_data)
            result = cursor.fetchone()

            return Person(**result)

    def delete(self, identifications: List[str]) -> Optional[List[Person]]:
        with self.get_cursor() as cursor:
            query = sql.SQL(
                """
                DELETE FROM person
                WHERE identification = ANY(%s)
                RETURNING *;
                """
            )

            cursor.execute(query, (identifications,))
            results = cursor.fetchall()

            return [Person(**fila) for fila in results] if results else None
