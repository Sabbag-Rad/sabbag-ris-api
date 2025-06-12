import logging
import os

logger = logging.getLogger(__name__)

DICOM_URL = os.environ.get("DICOM_URL")


def generate_dicom_url(payload: dict) -> dict:
    logger.info("[Service] Generando URL DICOM...")

    study_number = payload.get("study_number")
    username = payload.get("username")
    password = payload.get("password")

    if not study_number or not username or not password:
        logger.error("[Service] Faltan datos requeridos para generar la URL")
        raise ValueError("Faltan datos requeridos")

    url = f"{DICOM_URL}?user={username}&pass={password}&study={study_number}"

    logger.info(f"[Service] URL generada: {url}")

    return {"dicom_url": url}
