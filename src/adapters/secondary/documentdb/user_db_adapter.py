from aws_lambda_powertools import Logger

from src.db.constants import USER_COLLECTION_NAME
from src.repositories.document_db.client import create_documentdb_client as connect_to_db

logger = Logger()


class DocumentDBAdapter:
    def __init__(self):
        self._collection_name = USER_COLLECTION_NAME
        self._client = connect_to_db()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def get_collection(self, collection_name):
        return self._client[collection_name]
