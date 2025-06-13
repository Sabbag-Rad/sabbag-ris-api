from src.config.db import get_db_connection
import logging


logger = logging.getLogger(__name__)


def get_patient_by_credentials(document_type: str, document: str, password_hash: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_pac AS patient_id, 
                nm_pac AS patient_name,
                cpf_pac AS document_number, 
                tipo_doc1 AS document_type,
                FROM mediclinic.pacientes
                WHERE tipo_doc1 = %s AND cpf_pac = %s AND senhaweb = %s
            """,
                (document_type, document, password_hash),
            )
            row = cur.fetchone()

            if row:
                columns = [desc[0] for desc in cur.description]
                patient = dict(zip(columns, row))
                logger.debug(
                    f"[Repository] Patient found for ID {patient['patient_id']}"
                )
                return patient
            else:
                logger.warning(
                    f"[Repository] No patient found for document {document} and type {document_type}"
                )
                return None


def get_patient_by_document(document_type: str, document: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_pac AS patient_id,
                nm_pac AS patient_name,
                email_pac AS email, 
                tel1_pac AS phone1, 
                tel2_pac AS phone2,
                FROM mediclinic.pacientes
                WHERE tipo_doc1 = %s AND cpf_pac = %s
            """,
                (document_type, document),
            )
            row = cur.fetchone()

            if row:
                columns = [desc[0] for desc in cur.description]
                patient = dict(zip(columns, row))
                logger.debug(
                    f"[Repository] Patient found for document {document} and type {document_type}"
                )
                return patient
            else:
                logger.warning(
                    f"[Repository] No patient found for document {document} and type {document_type}"
                )
                return None


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
