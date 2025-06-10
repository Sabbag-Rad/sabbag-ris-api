import json
from src.schemas.auth_schemas import RecoveryOptionsSchema
from src.common.decorators.response import standard_response
from src.repositories.patient_repository import get_patient_by_document


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
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]

    row = get_patient_by_document(document_type, document)
    if not row:
        raise Exception("Patient not found")

    _, _, email, tel1, tel2 = row

    return {
        "email": mask_email(email),
        "phone1": mask_phone(tel1 or tel2),
    }
