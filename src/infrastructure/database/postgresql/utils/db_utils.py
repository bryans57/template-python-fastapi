from contextlib import contextmanager

from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor

from src.domain.exceptions.exceptions import DatabaseErrorHandling


@contextmanager
def get_db_cursor(db):
    """Generic context manager to handle database connections safely."""
    con = db.get_connection()
    try:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor
            con.commit()
    except DatabaseError as e:
        con.rollback()
        raise DatabaseErrorHandling(e) from e
    finally:
        db.put_connection(con)
