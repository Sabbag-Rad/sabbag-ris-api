import json
import logging
from src.schemas.auth_schemas import PasswordResetSchema
from src.common.decorators.auth import require_auth
from src.common.decorators.response import standard_response
from src.services.password_reset_service import reset_patient_password

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@require_auth(expected_purpose="password_reset")
@standard_response(
    schema_class=PasswordResetSchema,
    success_message="Contraseña actualizada correctamente",
)
def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    # Capturar y loggear campos no sensibles
    document_type = body.get("document_type")
    document = body.get("document")
    logger.info(
        f"[Handler] Password reset request received for document_type={document_type}, document={document}"
    )

    return reset_patient_password(body)
