import logging
from src.repositories.patient_repository import (
    get_patient_by_document,
    update_patient_password,
)
from src.common.utils.otp_utils import (
    generate_otp,
    store_otp,
    validate_otp,
    clear_otp,
    get_otp,
)
from src.common.auth.jwt import create_jwt_token
from src.common.utils.masking import mask_email, mask_phone

logger = logging.getLogger(__name__)


def get_recovery_options(document_type: str, document: str):
    logger.info("[Service] Getting recovery options")
    patient = get_patient_by_document(document_type, document)

    if not patient:
        raise ValueError("Patient not found")

    return {
        "email": mask_email(patient["email"]),
        "phone": mask_phone(patient["phone1"]),
    }


def send_recovery_otp(document_type: str, document: str, recovery_method: str):
    logger.info("[Service] Sending recovery OTP")
    patient = get_patient_by_document(document_type, document)

    if not patient:
        raise ValueError("Patient not found")

    otp = generate_otp()
    store_otp("password_recovery", patient["patient_id"], otp)

    if recovery_method not in ["email", "phone"]:
        raise ValueError("Invalid recovery method")

    if recovery_method == "email":
        logger.info(f"Send OTP {otp} to email {patient['email']}")
    elif recovery_method == "phone":
        logger.info(f"Send OTP {otp} to phone {patient['phone1'] or patient['phone2']}")

    return {"message": f"OTP sent via {recovery_method}"}


def verify_recovery_otp(document_type: str, document: str, otp: str):
    logger.info("[Service] Verifying recovery OTP")
    patient = get_patient_by_document(document_type, document)

    if not patient:
        raise ValueError("Patient not found")

    if not validate_otp("password_recovery", patient["patient_id"], otp):
        raise ValueError("Invalid or expired OTP")

    token = create_jwt_token(
        {
            "document_type": document_type,
            "document": document,
            "purpose": "password_reset",
        },
        expires_in_minutes=10,
    )

    clear_otp("password_recovery", patient["patient_id"])
    return {"message": "OTP verified successfully", "token": token}


def reset_password(payload: dict):
    document_type = payload["document_type"]
    document = payload["document"]
    new_password_encrypted = payload["new_password"]

    logger.info(
        f"[RecoveryService] Verificando paciente con document_type={document_type}, document={document}"
    )
    patient = get_patient_by_document(document_type, document)

    if not patient:
        logger.warning(
            f"[RecoveryService] Paciente no encontrado: {document_type}-{document}"
        )
        raise ValueError("Paciente no encontrado")

    patient_id = patient["patient_id"]
    logger.info(f"[RecoveryService] Paciente encontrado. ID: {patient_id}")

    logger.info(
        f"[RecoveryService] Actualizando contraseña para paciente ID: {patient_id}"
    )
    update_patient_password(patient_id, new_password_encrypted)
    logger.info(
        f"[RecoveryService] Contraseña actualizada para paciente ID: {patient_id}"
    )

    return {"message": "Contraseña actualizada correctamente"}
