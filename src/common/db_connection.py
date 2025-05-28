import psycopg2
from src.common.secrets import get_db_secret

def get_connection():
    secret = get_db_secret()
    conn = psycopg2.connect(
        host=secret["host"],
        port=secret["port"],
        user=secret["username"],
        password=secret["password"],
        dbname=secret["dbname"]
    )
    return conn