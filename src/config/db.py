import psycopg2
from contextlib import contextmanager
from src.common.aws.secret_utils import get_db_secret


@contextmanager
def get_db_connection():
    secret = get_db_secret()
    conn = psycopg2.connect(
        host=secret["host"],
        port=secret["port"],
        user=secret["username"],
        password=secret["password"],
        dbname=secret["dbname"],
    )
    try:
        yield conn
    finally:
        conn.close()
