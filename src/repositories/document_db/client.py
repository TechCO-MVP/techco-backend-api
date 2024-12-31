import os

import boto3
from aws_lambda_powertools import Logger
from pymongo import MongoClient
from pymongo.database import Database

from src.constants.index import REGION_NAME

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CERT_PATH = os.path.join(BASE_PATH, "../certs/global-bundle.pem")

logger = Logger()


def create_documentdb_client() -> Database:
    """
    Create a documentdb client
    return: The documentdb client for the database
    """
    logger.info("Creating documentdb client")
    logger.info("Getting certificate path from: %s", CERT_PATH)

    config = get_documentdb_config()
    username = config["username"]
    password = config["password"]
    cluster_endpoint = config["cluster_endpoint"]
    cluster_port = config["cluster_port"]
    database_name = config["database_name"]

    uri = (
        f"mongodb://{username}:{password}@{cluster_endpoint}:{cluster_port}/{database_name}"
        "?ssl=true&retryWrites=false"
    )
    client = MongoClient(uri, tls=True, tlsCAFile=CERT_PATH)

    return client.get_database(database_name)


def get_documentdb_config() -> dict:
    """
    Get the configuration for the documentdb client
    return: The configuration object
    """
    documentdb_secret_name = os.getenv("DOCUMENTDB_SECRET_NAME")

    return {
        "username": os.getenv("DOCUMENTDB_USERNAME"),
        "password": get_password_secret(documentdb_secret_name),
        "cluster_endpoint": os.getenv("DOCUMENTDB_ENDPOINT"),
        "cluster_port": os.getenv("DOCUMENTDB_PORT"),
        "database_name": os.getenv("DOCUMENTDB_DATABASE"),
    }


def get_password_secret(secret_name: str) -> str:
    """
    Get the password from the secret manager
    secret_name: The secret name
    """
    try:
        client = boto3.client("secretsmanager", region_name=REGION_NAME)
        response = client.get_secret_value(SecretId=secret_name)

        return response["SecretString"]
    except Exception as e:
        logger.exception(f"An error occurred while trying to get the secret {secret_name}")
        raise e
