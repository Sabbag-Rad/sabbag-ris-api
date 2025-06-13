import json
from src.schemas.auth_schemas import PatientLoginSchema
from src.services.login_service import login_patient
from src.common.decorators.response import standard_response


@standard_response(schema_class=PatientLoginSchema)
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    document_type = body["document_type"]
    document = body["document"]
    password = body["password"]

    patient = login_patient(document_type, document, password)

    if not patient:
        raise ValueError("Credenciales inválidas")

    return patient
