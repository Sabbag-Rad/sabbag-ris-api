def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return None
    local, domain = email.split("@")
    return f"{local[0]}***{local[-1]}@{domain}"


def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 5:
        return None
    return phone[:3] + "*" * (len(phone) - 5) + phone[-2:]
