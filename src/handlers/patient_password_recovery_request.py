import json
from src.schemas.auth_schemas import PasswordRecoveryRequestSchema
from src.common.decorators.response import standard_response
from src.repositories.patient_repository import get_patient_by_document
from src.services.otp_service import generate_otp, store_otp


@standard_response(schema_class=PasswordRecoveryRequestSchema)
def lambda_handler(event, context):
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
