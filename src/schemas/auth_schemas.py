from pydantic import BaseModel, Field


class PatientLoginSchema(BaseModel):
    document_type: str = Field(..., description="Tipo de documento del paciente")
    document: str = Field(..., description="Número de documento")
    password: str = Field(
        ..., description="Contraseña encriptada con SHA-512 desde el frontend"
    )


class RecoveryOptionsSchema(BaseModel):
    document_type: str = Field(..., max_length=5)
    document: str = Field(..., min_length=5, max_length=20)


class PasswordRecoveryRequestSchema(BaseModel):
    document_type: str = Field(..., max_length=5)
    document: str = Field(..., min_length=5, max_length=20)
    recovery_method: str = Field(..., pattern="^(email|phone)$")


class PasswordRecoveryVerifySchema(BaseModel):
    document_type: str = Field(..., max_length=5)
    document: str = Field(..., min_length=5, max_length=20)
    otp: str = Field(..., min_length=4, max_length=6)


class PasswordResetSchema(BaseModel):
    document_type: str = Field(..., max_length=5)
    document: str = Field(..., min_length=5, max_length=20)
    new_password: str = Field(..., min_length=8, max_length=128)


class UserLoginSchema(BaseModel):
    username: str = Field(..., example="jmedico")
    password: str = Field(..., example="sha512_encrypted_string")


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str
