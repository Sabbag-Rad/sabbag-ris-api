import logging
from functools import wraps
from src.common.auth.jwt import decode_jwt_token
from src.common.utils.exceptions import UnauthorizedError, ForbiddenError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def require_auth(expected_purpose=None):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            headers = event.get("headers", {})
            auth_header = headers.get("Authorization") or headers.get("authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                logger.warning(
                    "[Auth] Falta el token de autorización o está mal formado"
                )
                raise UnauthorizedError(
                    "Falta el token Bearer en el encabezado Authorization"
                )

            token = auth_header.split(" ")[1]
            logger.info(f"[Auth] Token recibido: {token[:20]}...")

            payload = decode_jwt_token(token)
            logger.info(f"[Auth] Payload decodificado: {payload}")

            if expected_purpose and payload.get("purpose") != expected_purpose:
                logger.warning(
                    f"[Auth] Purpose inválido: se esperaba '{expected_purpose}', se recibió '{payload.get('purpose')}'"
                )
                raise ForbiddenError("Purpose inválido en el token")

            event["auth"] = payload
            return func(event, context)

        return wrapper

    return decorator
