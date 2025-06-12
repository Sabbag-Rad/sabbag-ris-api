from pydantic import BaseModel
from typing import Optional


class IdName(BaseModel):
    id: str
    name: str


class DocumentType(IdName):
    abbreviation: str


class Patient(IdName):
    document_type: DocumentType
    document: str
    age: Optional[str]


class Physician(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    sign_url: Optional[str] = None
    crm: Optional[str] = None


class ReportSchema(BaseModel):
    patient: Patient
    study_number: str
    service: str
    date: str
    report_content: str
    interpreting_physician: Physician
    reviewing_physician: Optional[Physician] = None
    referring_physician: str


