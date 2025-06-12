from striprtf.striprtf import rtf_to_text
import logging

logging.basicConfig(level=logging.INFO)


def convert_rtf_to_text(rtf_content: str) -> str:
    try:
        plain_text = rtf_to_text(rtf_content)
        return plain_text.strip()
    except Exception as e:
        logging.error(f"[RTF Parser] Error al convertir RTF a texto: {str(e)}")
        raise ValueError("No se pudo convertir el contenido RTF a texto plano")
