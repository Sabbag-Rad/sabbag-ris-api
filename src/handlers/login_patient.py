import json
from src.schemas.auth_schemas import PatientLoginSchema
from src.services.login_service import login_patient
from src.common.auth.jwt import create_jwt_token
from src.common.decorators.response import standard_response


@standard_response(schema_class=PatientLoginSchema)
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    document_type = body["document_type"]
    document = body["document"]
    password = body["password"]

    patient = login_patient(document_type, document, password)

    if not patient:
        raise Exception("Credenciales inválidas")

    token = create_jwt_token(
        {"sub": patient["patient_id"], "role": "patient", "purpose": "patient_access"}
    )

    return {
        "user_id": patient["patient_id"],
        "name": patient["name"],
        "rol": "patient",
        "token": token,
    }
