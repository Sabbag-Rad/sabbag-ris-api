import json
from src.schemas.auth_schemas import (
    RecoveryOptionsSchema,
    PasswordRecoveryRequestSchema,
    PasswordRecoveryVerifySchema,
)
from src.common.auth.jwt import create_jwt_token
from src.common.decorators.response import standard_response
from src.repositories.patient_repository import get_patient_by_document
from src.services.otp_service import generate_otp, store_otp, validate_otp, clear_otp


def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return None
    local, domain = email.split("@")
    return f"{local[0]}***{local[-1]}@{domain}"


def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 5:
        return None
    return phone[:3] + "*" * (len(phone) - 5) + phone[-2:]


@standard_response(schema_class=RecoveryOptionsSchema)
def otp_options_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]

    row = get_patient_by_document(document_type, document)
    if not row:
        raise Exception("Patient not found")

    _, _, email, tel1, tel2 = row

    return {
        "email": mask_email(email),
        "phone": mask_phone(tel1 or tel2),
    }


@standard_response(schema_class=PasswordRecoveryRequestSchema)
def otp_request_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]
    recovery_method = body["recovery_method"]

    row = get_patient_by_document(document_type, document)
    if not row:
        raise Exception("Patient not found")

    patient_id, name, email, phone1, phone2 = row

    otp = generate_otp()

    store_otp(patient_id, otp)

    if recovery_method not in ["email", "phone"]:
        raise Exception("Invalid recovery method")

    if recovery_method == "email":
        print(f"Send OTP {otp} to email {email}")
    elif recovery_method == "phone":
        print(f"Send OTP {otp} to phone {phone1}")
    else:
        raise Exception("No recovery method configured")

    return {"message": f"OTP sent via {recovery_method}"}


@standard_response(schema_class=PasswordRecoveryVerifySchema)
def otp_verify_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]
    otp = body["otp"]

    row = get_patient_by_document(document_type, document)
    if not row:
        raise Exception("Patient not found")

    patient_id, *_ = row

    if not validate_otp(patient_id, otp):
        raise Exception("Invalid or expired OTP")

    token = create_jwt_token(
        {
            "document_type": document_type,
            "document": document,
            "purpose": "password_reset",
        },
        expires_in_minutes=10,
    )

    clear_otp(patient_id)

    if not token:
        raise Exception("Failed to create JWT token")

    return {"message": "OTP verified successfully", "token": token}
