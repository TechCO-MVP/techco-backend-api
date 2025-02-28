import boto3
import json

from aws_lambda_powertools import Logger
from src.constants.index import REGION_NAME


logger = Logger()


def get_secret_by_name(secret_name: str, format: str = "") -> dict:
    """
    Get the secret by name
    secret_name: The secret name
    """
    try:
        client = boto3.client("secretsmanager", region_name=REGION_NAME)
        response = client.get_secret_value(SecretId=secret_name)

        if format == "json":
            return json.loads(response["SecretString"])

        return response["SecretString"]
    except Exception as e:
        logger.error(f"Error getting secret {secret_name}: {e}")
        raise e
