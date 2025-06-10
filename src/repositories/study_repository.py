from src.config.db import get_db_connection


def get_patient_studies(patient_id, filters=None, limit=10, offset=0):
    query = """
        SELECT 
            ex.os_exame AS study_number,
            ex.data AS date,
            m.codigo AS modality_code,
            m.descricao AS modality_name,
            s.id_serv AS service_id,
            s.desc_serv AS service_name
        FROM mediclinic.exames ex
        JOIN mediclinic.servicos s ON ex.id_serv = s.id_serv
        JOIN mediclinic.modalidades m ON s.modalidade = m.codigo
        WHERE ex.id_pac = %s
    """
    params = [patient_id]

    if filters:
        if filters.get("service_name"):
            query += " AND s.desc_serv ILIKE %s"
            params.append(f"%{filters['service_name']}%")

        if filters.get("study_number"):
            query += " AND ex.os_exame ILIKE %s"
            params.append(f"%{filters['study_number']}%")

        if filters.get("modality"):
            modality = filters["modality"]
            if isinstance(modality, list):
                placeholders = ", ".join(["%s"] * len(modality))
                query += f" AND m.codigo IN ({placeholders})"
                params.extend(modality)
            else:
                query += " AND m.codigo = %s"
                params.append(modality)

        if filters.get("start_date"):
            query += " AND ex.data >= %s"
            params.append(filters["start_date"])

        if filters.get("end_date"):
            query += " AND ex.data <= %s"
            params.append(filters["end_date"])

    order_by = filters.get("order_by", "ex.data")
    if order_by == "date":
        order_by = "ex.data"
    elif order_by == "study_number":
        order_by = "ex.os_exame"
    elif order_by == "service_name":
        order_by = "s.desc_serv"
    elif order_by == "modality":
        order_by = "m.codigo"

    order = filters.get("order", "desc").upper()
    if order not in ("ASC", "DESC"):
        order = "DESC"

    query += f" ORDER BY {order_by} {order} LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def count_patient_studies(patient_id, filters=None):
    query = """
        SELECT COUNT(*)
        FROM mediclinic.exames ex
        JOIN mediclinic.servicos s ON ex.id_serv = s.id_serv
        JOIN mediclinic.modalidades m ON s.modalidade = m.codigo
        WHERE ex.id_pac = %s
    """
    params = [patient_id]

    if filters:
        if filters.get("service_name"):
            query += " AND s.desc_serv ILIKE %s"
            params.append(f"%{filters['service_name']}%")

        if filters.get("study_number"):
            query += " AND ex.os_exame ILIKE %s"
            params.append(f"%{filters['study_number']}%")

        if filters.get("modality"):
            modality = filters["modality"]
            if isinstance(modality, list):
                placeholders = ", ".join(["%s"] * len(modality))
                query += f" AND m.codigo IN ({placeholders})"
                params.extend(modality)
            else:
                query += " AND m.codigo = %s"
                params.append(modality)

        if filters.get("start_date"):
            query += " AND ex.data >= %s"
            params.append(filters["start_date"])

        if filters.get("end_date"):
            query += " AND ex.data <= %s"
            params.append(filters["end_date"])

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()[0]
