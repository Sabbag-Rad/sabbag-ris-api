import json
import logging
from src.schemas.auth_schemas import (
    RecoveryOptionsSchema,
    PasswordRecoveryRequestSchema,
    PasswordRecoveryVerifySchema,
    PasswordResetSchema,
)
from src.services.recovery_service import (
    get_recovery_options,
    send_recovery_otp,
    verify_recovery_otp,
    reset_password,
)
from src.common.decorators.response import standard_response
from src.common.decorators.auth import require_auth


logger = logging.getLogger(__name__)


@standard_response(schema_class=RecoveryOptionsSchema)
def recovery_options_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]

    return get_recovery_options(document_type, document)


@standard_response(schema_class=PasswordRecoveryRequestSchema)
def recovery_request_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]
    recovery_method = body["recovery_method"]

    return send_recovery_otp(document_type, document, recovery_method)


@standard_response(schema_class=PasswordRecoveryVerifySchema)
def recovery_verify_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    document_type = body["document_type"]
    document = body["document"]
    otp = body["otp"]

    return verify_recovery_otp(document_type, document, otp)


@require_auth(expected_purpose="password_reset")
@standard_response(schema_class=PasswordResetSchema)
def reset_password_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    logger.info(f"[Handler] Datos recibidos para reset password: {body}")
    return reset_password(body)
