import boto3
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SES_SENDER = os.environ.get("SES_SENDER", "no-reply@example.com")


def send_email(
    recipient: str, subject: str, body_text: str, body_html: str = None
) -> bool:
    client = boto3.client("ses", region_name=AWS_REGION)

    message = {
        "Subject": {"Data": subject, "Charset": "UTF-8"},
        "Body": {
            "Text": {"Data": body_text, "Charset": "UTF-8"},
        },
    }

    if body_html:
        message["Body"]["Html"] = {"Data": body_html, "Charset": "UTF-8"}

    try:
        response = client.send_email(
            Source=SES_SENDER,
            Destination={"ToAddresses": [recipient]},
            Message=message,
        )
        logger.info(
            f"[SES] Email sent to {recipient}: MessageId {response['MessageId']}"
        )
        return True
    except ClientError as e:
        logger.error(
            f"[SES] Failed to send email to {recipient}: {e.response['Error']['Message']}"
        )
        return False
