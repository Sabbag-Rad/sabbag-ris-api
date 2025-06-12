import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")


def upload_pdf_to_s3(pdf_path: str, bucket_name: str, object_key: str) -> str:
    """
    Sube el archivo PDF a S3 y retorna una URL presignada.
    :param pdf_path: Ruta local al archivo PDF (ej. /tmp/report_123.pdf)
    :param bucket_name: Nombre del bucket S3
    :param object_key: Ruta del objeto en S3 (ej. reports/2025/report_123.pdf)
    :return: URL presignada del archivo en S3 (válida por 1 hora)
    """
    try:
        logger.info(f"[S3] Subiendo {pdf_path} a s3://{bucket_name}/{object_key}")
        s3_client.upload_file(pdf_path, bucket_name, object_key)

        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )

        logger.info(f"[S3] Archivo subido exitosamente. URL presignada: {url}")
        return url

    except (BotoCoreError, ClientError) as e:
        logger.error(f"[S3] Error subiendo a S3: {str(e)}")
        raise
