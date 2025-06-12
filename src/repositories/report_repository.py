from src.config.db import get_db_connection
import logging

logger = logging.getLogger(__name__)


def get_report_by_id(report_id: str):
    logger.info(f"[Repository] Getting report with ID: {report_id}")

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    p.id_pac AS patient_id,
                    p.nm_pac AS patient_name,
                    p.cpf_pac AS document_number,
                    p.tipo_doc1 AS document_type_id,
                    td.descricao AS document_type_name,
                    td.sigla AS document_type_abbreviation,
                    p.dtnasc_pac AS birth_date,
                    lf.servico AS service_name,
                    lf.data_exame AS study_date,
                    lf.num_exame AS study_number,
                    lf.desc_lfinal AS report_content,
                    ip.id_med AS interpreting_physician_id,
                    ip.nm_med AS interpreting_physician_name,
                    ip.crm_med AS interpreting_physician_crm,
                    rp.id_med AS reviewing_physician_id,
                    rp.nm_med AS reviewing_physician_name,
                    rp.crm_med AS reviewing_physician_crm,
                    lf.medico_solicitante AS referring_physician
                FROM mediclinic.laudos_finais lf
                LEFT JOIN mediclinic.pacientes p ON CAST(lf.patientid AS INTEGER) = p.id_pac
                LEFT JOIN mediclinic.tipos_documentos td ON p.tipo_doc1 = td.codigo
                LEFT JOIN mediclinic.medicos ip ON lf.id_med_emit = ip.id_med
                LEFT JOIN mediclinic.medicos rp ON lf.id_med_rev = rp.id_med
                WHERE lf.num_exame = %s
                """,
                (report_id,),
            )

            report = cur.fetchone()

            if report:
                logger.debug(f"[Repository] Report found for ID {report_id}")
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, report))
            else:
                logger.warning(f"[Repository] No report found for ID {report_id}")
                return None
