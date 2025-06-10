from src.config.db import get_db_connection


def get_user_by_credentials(username: str, password_hash: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT usuario, nome
                FROM mediweb.usuario
                WHERE  usuario= %s  AND senha = %s AND habilitado = 'T'
            """,
                (username, password_hash),
            )
            row = cur.fetchone()
    return row
