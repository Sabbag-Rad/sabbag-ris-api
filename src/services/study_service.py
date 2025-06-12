from src.repositories.study_repository import (
    get_studies_by_patient_id,
    count_studies_by_patient_id,
)
from src.schemas.study_schemas import StudySchema
import logging

logger = logging.getLogger(__name__)


def get_studies(patient_id: str, filters: dict, limit: int, offset: int):
    logger.info(f"[Service] Getting studies for patient ID: {patient_id}")

    rows = get_studies_by_patient_id(patient_id, filters, limit, offset)
    total = count_studies_by_patient_id(patient_id, filters)

    total_pages = (total // limit) + int(total % limit > 0)

    items = (
        [
            StudySchema(
                study_number=row["study_number"],
                date=row["date"].isoformat(),
                modality={"id": str(row["modality_id"]), "name": row["modality_name"]},
                service={"id": str(row["service_id"]), "name": row["service_name"]},
            ).dict()
            for row in rows
        ]
        if rows
        else []
    )

    return {
        "data": items,
        "pagination": {
            "page": (offset // limit) + 1,
            "per_page": limit,
            "total_pages": total_pages,
            "total_items": total,
        },
    }
