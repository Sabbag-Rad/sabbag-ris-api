from functools import wraps
from src.common.db_connection import get_connection

def with_db_connection(handler):
    @wraps(handler)
    def wrapper(event, context):
        conn = None
        try:
            conn = get_connection()
            result = handler(event, context, conn)
            return result
        finally:
            if conn:
                conn.close()
    return wrapper
