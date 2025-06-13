from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os
import logging

logger = logging.getLogger(__name__)


def render_report_html(report: dict) -> str:
    """
    Carga y renderiza la plantilla HTML con los datos del informe.
    Retorna un string HTML renderizado y guarda una copia en el directorio PDFs.
    """
    try:
        templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template("report_template.html")

        rendered_html = template.render(report=report)
        if not rendered_html:
            raise ValueError("Error al renderizar la plantilla HTML del informe")

        logger.info(
            f"[PDF Service] Report HTML rendered successfully for report ID: {report.get('study_number', 'unknown')}"
        )

        return rendered_html

    except Exception as e:
        logger.error(f"[PDF Service] Error rendering or saving HTML: {str(e)}")
        raise


def generate_pdf_from_html(html_content: str, output_path: str):
    try:
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if pisa_status.err:
            raise ValueError("Error al generar el PDF con xhtml2pdf")

        logger.info(f"[PDF Service] PDF generated with xhtml2pdf at {output_path}")
    except Exception as e:
        logger.error(f"[PDF Service] Failed to generate PDF: {str(e)}")
        raise ValueError("Fallo al generar el PDF desde HTML con xhtml2pdf")
