import json
from src.schemas.auth_schemas import PasswordRecoveryVerifySchema
from src.common.decorators.response import standard_response
from src.common.auth.jwt import create_jwt_token
from src.repositories.patient_repository import get_patient_by_document
from src.services.otp_service import validate_otp


@standard_response(schema_class=PasswordRecoveryVerifySchema)
def lambda_handler(event, context):
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

    return {"message": "OTP verified successfully", "token": token}
