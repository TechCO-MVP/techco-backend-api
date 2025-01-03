import os
import json

import boto3
from aws_lambda_powertools import Logger
from pymongo import MongoClient
from pymongo.database import Database

logger = Logger()


def create_documentdb_client() -> Database:
    """
    Create a documentdb client
    return: The documentdb client for the database
    """
    logger.info("Creating documentdb client")

    config = get_documentdb_config()
    username = config["username"]
    password = config["password"]
    cluster_endpoint = config["cluster_endpoint"]
    cluster_port = config["cluster_port"]
    database_name = config["database_name"]

    uri = (
        f"mongodb://{username}:{password}@{cluster_endpoint}:{cluster_port}/"
        "?tls=true"
        "&replicaSet=rs0"
        "&readPreference=secondaryPreferred"
        "&retryWrites=false"
        "&authSource=admin"
    )
    client = MongoClient(uri, tls=True, tlsCAFile="./certs/global-bundle.pem")

    return client.get_database(database_name)


def get_documentdb_config() -> dict:
    """
    Get the configuration for the documentdb client
    return: The configuration object
    """
    documentdb_secret_name = os.getenv("DOCUMENTDB_SECRET_NAME")
    secret_value = get_user_password_secret(documentdb_secret_name)

    return {
        "username": secret_value["username"],
        "password": secret_value["password"],
        "cluster_endpoint": os.getenv("DOCUMENTDB_ENDPOINT"),
        "cluster_port": os.getenv("DOCUMENTDB_PORT"),
        "database_name": os.getenv("DOCUMENTDB_DATABASE"),
    }


def get_user_password_secret(secret_name: str) -> dict:
    """
    Get the password from the secret manager
    secret_name: The secret name
    """
    try:
        client = boto3.client("secretsmanager", region_name=os.getenv("REGION_NAME"))
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response["SecretString"]

        return json.loads(secret_string)
    except Exception as e:
        logger.exception(f"An error occurred while trying to get the secret {secret_name}")
        raise e
