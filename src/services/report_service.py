import os
import logging
from src.common.utils.pdf_utils import render_report_html, generate_pdf_from_html
from src.common.aws.s3_utils import upload_pdf_to_s3
from src.repositories.report_repository import get_report_by_id
from src.schemas.report_schemas import ReportSchema
from src.common.utils.rtf2text import convert_rtf_to_text

logger = logging.getLogger(__name__)


def get_report(report_id: str):
    logger.info(f"[Service] Processing report ID: {report_id}")
    report = get_report_by_id(report_id)

    if not report:
        logger.error(f"[Service] Report ID {report_id} not found in repository")
        return None

    age = None

    raw_bytes = report["report_content"]
    if isinstance(raw_bytes, memoryview):
        raw_bytes = raw_bytes.tobytes()

    try:
        rtf_str = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        rtf_str = raw_bytes.decode("latin-1", errors="replace")

    report_content = convert_rtf_to_text(rtf_str)

    report_dict = ReportSchema(
        patient={
            "id": str(report["patient_id"]),
            "name": report["patient_name"],
            "document_type": {
                "id": str(report["document_type_id"]),
                "name": report["document_type_name"],
                "abbreviation": report["document_type_abbreviation"],
            },
            "document": report["document_number"],
            "age": age,
        },
        study_number=report["study_number"],
        service=report["service_name"],
        date=report["study_date"].isoformat(),
        report_content=report_content,
        interpreting_physician={
            "id": str(report["interpreting_physician_id"]),
            "name": report["interpreting_physician_name"],
            "crm": report["interpreting_physician_crm"],
        },
        reviewing_physician={
            "id": str(report["reviewing_physician_id"]),
            "name": report["reviewing_physician_name"],
            "crm": report["reviewing_physician_crm"],
        },
        referring_physician=report["referring_physician"],
    ).dict()

    return report_dict


def generate_report_pdf(report_id: str) -> dict:
    logger.info(f"[Service] Generating PDF for report ID: {report_id}")

    report = get_report(report_id)
    if not report:
        logger.warning(f"[Service] Report not found: {report_id}")
        raise ValueError("Informe no encontrado")

    try:
        html_content = render_report_html(report)
        pdf_filename = f"{report_id}.pdf"
        pdf_path = f"/tmp/{pdf_filename}"

        generate_pdf_from_html(html_content, pdf_path)

        bucket_name = os.environ["S3_BUCKET"]
        object_key = f"reports/{pdf_filename}"
        pdf_url = upload_pdf_to_s3(pdf_path, bucket_name, object_key)

    except Exception as e:
        logger.error(f"[Service] Error generating or uploading PDF: {str(e)}")
        raise ValueError("Error al generar el PDF del informe")

    logger.info(f"[Service] PDF generated and uploaded successfully for: {report_id}")
    return {"pdf_url": pdf_url}
