import logging
from src.common.decorators.response import standard_response
from src.services.report_service import generate_report_pdf

logger = logging.getLogger(__name__)


@standard_response(success_message="Informe obtenido correctamente")
def lambda_handler(event, context):
    report_id = event.get("pathParameters", {}).get("report_id")

    if not report_id:
        logger.error("[Handler] report_id is missing from path parameters")
        raise ValueError("El ID del informe es requerido")
    else:
        logger.info(f"[Handler] Request received for report_id: {report_id}")

    result = generate_report_pdf(report_id)

    logger.info(
        f"[Handler] Report processed and PDF uploaded for report_id: {report_id}"
    )

    return result
