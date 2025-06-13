import os
import boto3
import json


def get_db_secret():
    secret_arn = os.environ["DB_MEDILAB_SECRET_ARN"]
    region = os.environ.get("AWS_REGION", "us-east-1")

    client = boto3.client("secretsmanager", region_name=region)
    secret_response = client.get_secret_value(SecretId=secret_arn)
    return json.loads(secret_response["SecretString"])
