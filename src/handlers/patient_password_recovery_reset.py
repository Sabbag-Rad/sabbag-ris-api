import json
import hashlib
from src.schemas.auth_schemas import PasswordResetSchema
from src.common.decorators.auth import require_auth
from src.common.decorators.response import standard_response
from src.repositories.patient_repository import (
    get_patient_by_document,
    update_patient_password,
)
from src.services.otp_service import get_otp, clear_otp


@require_auth(expected_purpose="password_reset")
@standard_response(schema_class=PasswordResetSchema)
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]
    new_password_encrypted = body["new_password"]

    row = get_patient_by_document(document_type, document)
    if not row:
        raise Exception("Patient not found")

    patient_id, *_ = row

    otp_stored = get_otp(patient_id)
    if not otp_stored:
        raise Exception("OTP validation required before resetting password")

    # Desencriptar y guardar como texto plano
    #new_password = hashlib.sha512(new_password_encrypted.encode("utf-8")).hexdigest()
    
    new_password = new_password_encrypted

    update_patient_password(patient_id, new_password)
    clear_otp(patient_id)

    return {"message": "Password updated successfully"}
