import jwt
import os
import datetime
import logging

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

    logger.info(f"JWT Payload: {payload}")

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    logger.info(f"Generated JWT Token: {token}")

    return token


def decode_jwt_token(token: str):
    
    if not token or len(token.split(".")) != 3:
        raise Exception("Token format invalid")
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
