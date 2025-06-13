import hashlib
import logging
from src.repositories.patient_repository import get_patient_by_credentials
from src.repositories.user_repository import get_user_by_credentials
from src.common.auth.jwt import create_jwt_token

logger = logging.getLogger(__name__)


def decrypt_sha512(encrypted: str) -> str:
    return hashlib.sha512(encrypted.encode("utf-8")).hexdigest()


def login_patient(document_type: str, document: str, encrypted_password: str):
    logger.info(
        f"[LoginService] Intentando autenticar paciente: {document_type}-{document}"
    )

    password_hash = encrypted_password  # ya viene encriptado desde frontend
    row = get_patient_by_credentials(document_type, document, password_hash)

    if not row:
        logger.warning(
            f"[LoginService] Credenciales inválidas para paciente {document_type}-{document}"
        )
        return None

    patient_id, name, document, doc_type = row

    token = create_jwt_token(
        {
            "sub": str(patient_id),
            "name": name,
            "role": "patient",
            "purpose": "patient_access",
        }
    )

    logger.info(
        f"[LoginService] Paciente autenticado correctamente: {name} ({patient_id})"
    )

    return {
        "user_id": patient_id,
        "name": name,
        "document": document,
        "document_type": doc_type,
        "role": "patient",
        "token": token,
    }


def login_user(username: str, encrypted_password: str):
    logger.info(f"[LoginService] Intentando autenticar usuario: {username}")

    password_hash = encrypted_password
    row = get_user_by_credentials(username, password_hash)

    if not row:
        logger.warning(
            f"[LoginService] Credenciales inválidas para usuario: {username}"
        )
        return None

    username, name = row

    token = create_jwt_token({"sub": username, "name": name, "role": "user"})

    logger.info(f"[LoginService] Usuario autenticado correctamente: {username}")

    return {"username": username, "name": name, "role": "user", "token": token}
