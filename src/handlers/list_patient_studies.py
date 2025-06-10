from src.common.decorators.auth import require_auth
from src.common.decorators.response import standard_response
from src.repositories.study_repository import get_patient_studies, count_patient_studies
from src.schemas.study_schemas import StudySchema


#@require_auth(expected_purpose="patient_access")
@standard_response(success_message="Listado de estudios obtenido correctamente")
def lambda_handler(event, context):
    patient_id = event.get("pathParameters", {}).get("patient_id")
    if not patient_id:
        raise ValueError("El ID del paciente es requerido")

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

    rows = get_patient_studies(patient_id, filters, limit, offset)
    total = count_patient_studies(patient_id, filters)
    total_pages = (total // limit) + int(total % limit > 0)

    items = [
        StudySchema(
            study_number=row[0],
            date=row[1].isoformat(),
            service={"id": str(row[4]), "name": row[5]},
            modality={"id": str(row[2]), "name": row[3]},
            pdf_url="https://example.com/studies/pdf/",
            image_url="https://example.com/studies/image/",
        ).dict()
        for row in rows
    ]

    return {
        "data": items,
        "pagination": {
            "page": page,
            "per_page": limit,
            "total_pages": total_pages,
            "total_items": total,
        },
    }
