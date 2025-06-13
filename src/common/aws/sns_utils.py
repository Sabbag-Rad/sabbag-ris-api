import boto3
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def send_sms(phone_number: str, message: str) -> bool:
    client = boto3.client("sns", region_name=AWS_REGION)

    try:
        response = client.publish(
            PhoneNumber=phone_number,
            Message=message,
        )
        logger.info(
            f"[SNS] SMS enviado a {phone_number}: MessageId {response['MessageId']}"
        )
        return True
    except ClientError as e:
        logger.error(
            f"[SNS] Error enviando SMS a {phone_number}: {e.response['Error']['Message']}"
        )
        return False
