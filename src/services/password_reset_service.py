import logging
from src.repositories.patient_repository import (
    get_patient_by_document,
    update_patient_password,
)
from src.services.otp_service import get_otp, clear_otp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def reset_patient_password(payload: dict):
    document_type = payload["document_type"]
    document = payload["document"]
    new_password_encrypted = payload["new_password"]

    logger.info(
        f"[Service] Verificando paciente con document_type={document_type}, document={document}"
    )
    row = get_patient_by_document(document_type, document)

    if not row:
        logger.warning(f"[Service] Paciente no encontrado: {document_type}-{document}")
        raise ValueError("Paciente no encontrado")

    patient_id, *_ = row
    logger.info(f"[Service] Paciente encontrado. ID: {patient_id}")

    logger.info(f"[Service] Verificando OTP para el paciente ID: {patient_id}")
    otp = get_otp(patient_id)
    if not otp:
        logger.warning(
            f"[Service] OTP no encontrado o no verificado para paciente ID: {patient_id}"
        )
        raise ValueError("OTP no verificado o expirado")

    logger.info(f"[Service] Actualizando contraseña para paciente ID: {patient_id}")
    update_patient_password(patient_id, new_password_encrypted)

    logger.info(f"[Service] Limpiando OTP para paciente ID: {patient_id}")
    clear_otp(patient_id)

    return {"message": "Password updated successfully"}
