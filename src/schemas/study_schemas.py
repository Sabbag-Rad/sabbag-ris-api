from pydantic import BaseModel
from typing import Optional


class IdName(BaseModel):
    id: str
    name: str


class StudySchema(BaseModel):
    study_number: str
    service: IdName
    date: str
    modality: IdName
