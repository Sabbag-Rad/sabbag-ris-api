import hashlib
from src.repositories.patient_repository import get_patient_by_credentials
from src.repositories.user_repository import get_user_by_credentials

def decrypt_sha512(encrypted: str) -> str:
    return hashlib.sha512(encrypted.encode("utf-8")).hexdigest()


def login_patient(document_type: str, document: str, encrypted_password: str):
    #password_hash = decrypt_sha512(encrypted_password)
    password_hash = encrypted_password  # Assuming the password is already hashed
    
    row = get_patient_by_credentials(document_type, document, password_hash)
    if not row:
        return None

    patient_id, name, document, doc_type = row
    return {
        "patient_id": patient_id,
        "name": name,
        "document": document,
        "document_type": doc_type
    }
    
def login_user(username: str, encrypted_password: str):
    #password_hash = decrypt_sha512(encrypted_password)
    password_hash = encrypted_password  # Assuming the password is already hashed
    
    row = get_user_by_credentials(username, password_hash)
    if not row:
        return None

    username, name = row
    
    return {
        "username": username,
        "name": name
    }

