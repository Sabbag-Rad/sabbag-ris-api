from pydantic import BaseModel, Field


class DicomRequestSchema(BaseModel):
    study_number: str = Field(..., description="Número del estudio")
    username: str = Field(..., description="Usuario del sistema DICOM")
    password: str = Field(..., description="Contraseña del sistema DICOM")
