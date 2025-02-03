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
                con.commit()

                results = cursor.fetchall()
                result_convert = [Person(**fila) for fila in results]
                return result_convert
        except DatabaseError as e:
            raise DatabaseErrorHandling(e) from e
        finally:
            self.db.put_connection(con)

    def add_person(self, person: Person) -> Person:
        con = self.db.get_connection()
        try:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                # Convert person to a dictionary
                person_data = person.model_dump()
                fields, values = list(person_data.keys()), list(person_data.values())

                # Create SQL for fields and placeholders
                fields_set = sql.SQL(", ").join(map(sql.Identifier, fields))
                placeholders = sql.SQL(", ").join(sql.Placeholder() for _ in fields)

                query = sql.SQL(
                    """
                    INSERT INTO person ({fields})
                    VALUES ({placeholders})
                    RETURNING *;
                    """
                ).format(fields=fields_set, placeholders=placeholders)

                # Log query
                full_query = cursor.mogrify(query.as_string(con), values)
                print(full_query.decode("utf-8"))

                # Execute query with values
                cursor.execute(query, values)
                con.commit()
                result = cursor.fetchone()

                return Person(**result)
        except DatabaseError as e:
            raise DatabaseErrorHandling(e) from e
        finally:
            self.db.put_connection(con)

    def update_person(self, person: Person) -> Person:
        con = self.db.get_connection()
        try:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                # Convert person to a dictionary
                person_data = person.model_dump()
                filtered_person_data = {k: v for k, v in person_data.items() if k != "identification" and v is not None}
                dict_values_person = filtered_person_data.items()

                query = sql.SQL(
                    """
                    UPDATE person
                    SET {fields}
                    WHERE identification = {identification}
                    RETURNING *;
                    """
                ).format(
                    fields=sql.SQL(", ").join(
                        sql.Composed([sql.Identifier(field), sql.SQL(" = "), sql.Literal(value)])
                        for field, value in dict_values_person
                    ),
                    identification=sql.Literal(person.identification),
                )

                # Log query
                full_query = cursor.mogrify(query.as_string(con), dict_values_person)
                print(full_query.decode("utf-8"))

                # Execute query with values
                cursor.execute(query, dict_values_person)
                con.commit()
                result = cursor.fetchone()

                return Person(**result)
        except DatabaseError as e:
            raise DatabaseErrorHandling(e) from e
        finally:
            self.db.put_connection(con)
