import boto3
import logging
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")


def upload_file_to_s3(path: str, bucket_name: str, object_key: str) -> str:
    try:
        logger.info(f"[S3] Subiendo {path} a s3://{bucket_name}/{object_key}")
        s3_client.upload_file(path, bucket_name, object_key)

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
