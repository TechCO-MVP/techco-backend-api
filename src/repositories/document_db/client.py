import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.client_session import ClientSession


from src.db.database_client import IDatabaseClient
from src.repositories.document_db.utils import create_documentdb_client


class DocumentDBClient(IDatabaseClient):
    _instance: "DocumentDBClient" = None
    _client: MongoClient
    _session: ClientSession = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentDBClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._client = create_documentdb_client()

    def get_client(self):
        return self._client

    def connect(self):
        return self

    def disconnect(self):
        self._client.close()
        DocumentDBClient._instance = None

    def get_session(self):
        return self._session

    def set_session(self, session: ClientSession):
        if self._session is not None:
            raise Exception("Session is already initialized.")
        self._session = session

    def close_session(self):
        if self._session is None:
            raise Exception("Session is not initialized.")
        self._session.abort_transaction()
        self._session.end_session()
        self._session = None

    @staticmethod
    def create_documentdb_database_client(database_name: str = None) -> Database:
        """
        Create a documentdb database client
        """
        client = DocumentDBClient().get_client()

        database_name = database_name or os.getenv("DOCUMENTDB_DATABASE")

        return client.get_database(database_name)
