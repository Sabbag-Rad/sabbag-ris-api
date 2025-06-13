import jwt
import os
import datetime
import logging
from src.common.utils.exceptions import UnauthorizedError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = "HS512"
DEFAULT_EXP_MINUTES = int(os.environ.get("JWT_EXPIRES_MINUTES", 60))


def create_jwt_token(data: dict, expires_in_minutes: int = DEFAULT_EXP_MINUTES):
    now = datetime.datetime.utcnow()

    try:
        minutes = int(expires_in_minutes)
    except (TypeError, ValueError):
        minutes = DEFAULT_EXP_MINUTES

    exp = now + datetime.timedelta(minutes=minutes)
    payload = {**data, "iat": now, "exp": exp}

    logger.debug(f"[JWT] Payload to encode: {payload}")

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    logger.info("[JWT] Token generado correctamente")
    return token


def decode_jwt_token(token: str):
    if not token or len(token.split(".")) != 3:
        logger.warning("[JWT] Token mal formado")
        raise UnauthorizedError("Token mal formado")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        logger.info("[JWT] Token decodificado correctamente")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("[JWT] Token expirado")
        raise UnauthorizedError("Token expirado")
    except jwt.InvalidTokenError as e:
        logger.warning(f"[JWT] Token inválido: {str(e)}")
        raise UnauthorizedError("Token inválido")
