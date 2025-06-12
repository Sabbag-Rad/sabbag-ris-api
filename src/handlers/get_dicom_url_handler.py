import json
import logging
from src.common.decorators.response import standard_response
from src.schemas.dicom_schemas import DicomRequestSchema
from src.services.dicom_service import generate_dicom_url

logger = logging.getLogger(__name__)


@standard_response(
    schema_class=DicomRequestSchema, success_message="DICOM URL generado correctamente"
)
def lambda_handler(event, context):
    raw_body = event.get("body", "{}")
    try:
        body = json.loads(raw_body)
    except json.JSONDecodeError as e:
        logger.error(f"[Handler] Error al parsear el body JSON: {str(e)}")
        raise ValueError("Formato de body inválido")

    logger.info(f"[Handler] Event body received: {body}")

    result = generate_dicom_url(body)
    logger.info("[Handler] DICOM URL generado correctamente")

    return result
