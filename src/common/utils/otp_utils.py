import random
import os
import logging
from typing import Union
from src.config.redis import get_redis_connection

logger = logging.getLogger(__name__)
r = get_redis_connection()
identifier = os.environ.get("REDIS_IDENTIFIER", "sabbag")


def generate_otp(length: int = 6) -> str:
    otp = "".join(str(random.randint(0, 9)) for _ in range(length))
    logger.debug(f"[OTP] OTP generado: {otp}")
    return otp


def build_otp_key(purpose: str, key_id: Union[str, int]) -> str:
    return f"{identifier}:otp:{purpose}:{key_id}"


def store_otp(purpose: str, key_id: Union[str, int], otp: str, ttl_seconds: int = 180):
    key = build_otp_key(purpose, key_id)
    r.setex(key, ttl_seconds, otp)
    logger.info(f"[OTP] OTP almacenado: {otp} para clave {key}")


def get_otp(purpose: str, key_id: Union[str, int]):
    key = build_otp_key(purpose, key_id)
    otp = r.get(key)
    logger.debug(f"[OTP] OTP recuperado para {key}: {otp}")
    return otp


def validate_otp(purpose: str, key_id: Union[str, int], otp: str) -> bool:
    stored_otp = get_otp(purpose, key_id)
    valid = stored_otp == otp
    logger.info(f"[OTP] Validación OTP para {purpose}:{key_id}: {valid}")
    return valid


def clear_otp(purpose: str, key_id: Union[str, int]):
    key = build_otp_key(purpose, key_id)
    r.delete(key)
    logger.info(f"[OTP] OTP eliminado para {key}")
