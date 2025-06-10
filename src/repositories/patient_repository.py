from src.config.db import get_db_connection


def get_patient_by_credentials(document_type: str, document: str, password_hash: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_pac, nm_pac, cpf_pac, tipo_doc1
                FROM mediclinic.pacientes
                WHERE tipo_doc1 = %s AND cpf_pac = %s AND senhaweb = %s
            """,
                (document_type, document, password_hash),
            )
            row = cur.fetchone()
    return row


def get_patient_by_document(document_type: str, document: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_pac, nm_pac, email_pac, tel1_pac, tel2_pac
                FROM mediclinic.pacientes
                WHERE tipo_doc1 = %s AND cpf_pac = %s
            """,
                (document_type, document),
            )
            return cur.fetchone()


def update_patient_password(patient_id: int, new_password: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE mediclinic.pacientes
                SET senhaweb = %s
                WHERE id_pac = %s
            """,
                (new_password, patient_id),
            )
            conn.commit()
