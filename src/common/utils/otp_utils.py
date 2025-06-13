import random
import os
import logging
from src.config.redis import get_redis_connection

logger = logging.getLogger(__name__)
r = get_redis_connection()
identifier = os.environ.get("REDIS_IDENTIFIER", "sabbag")


def generate_otp(length: int = 6) -> str:
    """Genera un código OTP numérico aleatorio."""
    otp = "".join(str(random.randint(0, 9)) for _ in range(length))
    logger.debug(f"[OTP] OTP generado: {otp}")
    return otp


def build_otp_key(purpose: str, key_id: str | int) -> str:
    """Crea una clave única para el OTP en Redis."""
    return f"{identifier}:otp:{purpose}:{key_id}"


def store_otp(purpose: str, key_id: str | int, otp: str, ttl_seconds: int = 180):
    """Guarda un OTP en Redis con TTL."""
    key = build_otp_key(purpose, key_id)
    r.setex(key, ttl_seconds, otp)
    logger.info(f"[OTP] OTP almacenado: {otp} para clave {key}")


def get_otp(purpose: str, key_id: str | int):
    """Recupera el OTP almacenado en Redis."""
    key = build_otp_key(purpose, key_id)
    otp = r.get(key)
    logger.debug(f"[OTP] OTP recuperado para {key}: {otp}")
    return otp


def validate_otp(purpose: str, key_id: str | int, otp: str) -> bool:
    """Valida un OTP dado contra el valor almacenado."""
    stored_otp = get_otp(purpose, key_id)
    valid = stored_otp == otp
    logger.info(f"[OTP] Validación OTP para {purpose}:{key_id}: {valid}")
    return valid


def clear_otp(purpose: str, key_id: str | int):
    """Elimina el OTP almacenado."""
    key = build_otp_key(purpose, key_id)
    r.delete(key)
    logger.info(f"[OTP] OTP eliminado para {key}")
