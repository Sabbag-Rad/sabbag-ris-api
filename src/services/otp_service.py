import random
import os
from src.common.cache.redis import get_redis_connection


r = get_redis_connection()

identifier = os.environ.get("REDIS_IDENTIFIER", "sabbag")

def generate_otp(length=6):
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def store_otp(patient_id: int, otp: str, ttl_seconds=180):
    key = f"{identifier}:otp:recovery:{patient_id}"
    r.setex(key, ttl_seconds, otp)
    print(f"Stored OTP {otp} for patient {patient_id} with key {key}")


def get_otp(patient_id: int):
    return r.get(f"{identifier}:otp:recovery:{patient_id}")


def validate_otp(patient_id: int, otp: str) -> bool:
    stored_otp = get_otp(patient_id)
    print (f"Validating OTP {otp} for patient {patient_id}, stored OTP: {stored_otp}")
    return stored_otp == otp


def clear_otp(patient_id: int):
    r.delete(f"{identifier}:otp:recovery:{patient_id}")
