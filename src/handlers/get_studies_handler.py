import logging
from src.common.decorators.auth import require_auth
from src.common.decorators.response import standard_response
from src.services.study_service import get_studies

logger = logging.getLogger(__name__)


# @require_auth(expected_purpose="patient_access")
@standard_response(success_message="Listado de estudios obtenido correctamente")
def lambda_handler(event, context):
    patient_id = event.get("pathParameters", {}).get("patient_id")

    if not patient_id:
        logger.error(f"[Handler] patient_id is missing from path parameters")
        raise ValueError("El ID del paciente es requerido")
    else:
        logger.info(f"[Handler] Request received for patient_id: {patient_id}")

    query_params = event.get("queryStringParameters") or {}

    modality = query_params.get("modality")
    if modality and isinstance(modality, str):
        modality = modality.split(",")

    filters = {
        "service_name": query_params.get("service_name"),
        "study_number": query_params.get("study_number"),
        "modality": modality,
        "start_date": query_params.get("start_date"),
        "end_date": query_params.get("end_date"),
        "order_by": query_params.get("order_by", "date"),
        "order": query_params.get("order", "desc"),
    }

    page = int(query_params.get("page", 1))
    limit = int(query_params.get("limit", 10))
    offset = (page - 1) * limit

    result = get_studies(patient_id, filters, limit, offset)

    logger.info(f"[Handler] List studies for patient_id: {patient_id}")

    return result
