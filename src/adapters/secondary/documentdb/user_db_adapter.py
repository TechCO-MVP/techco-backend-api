import os
from aws_lambda_powertools import Logger
from src.repositories.document_db.client import create_documentdb_client as connect_to_db

logger = Logger()

class DocumentDBAdapter:
    def __init__(self):
        self._collection_name = "user"
        self._client = connect_to_db()
        database_name = os.getenv("DOCUMENTDB_DATABASE")
        self.db = self._client[database_name]

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    


