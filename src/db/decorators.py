from aws_lambda_powertools import Logger
from src.repositories.document_db.client import DocumentDBClient

logger = Logger()


def db_client(func):
    def wrapper(event, context, *args, **kwargs):
        logger.info("Creating db client")
        DocumentDBClient()
        return func(event, context, *args, **kwargs)

    return wrapper
