from pydantic import BaseModel
from typing import Optional


class EntitySchema(BaseModel):
    id: str
    name: str


class StudySchema(BaseModel):
    study_number: str
    service: EntitySchema
    date: str
    modality: EntitySchema
    pdf_url: Optional[str]
    image_url: Optional[str]
