from pymongo.database import Database

from src.repositories.document_db.client import create_documentdb_client
from src.repositories.repository import IRepository
from src.domain.business import BusinessEntity


class BusinessDocumentDBAdapter(IRepository[BusinessEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        self._collection_name = "business"
        self._client = create_documentdb_client()

    def getAll(self):
        collection = self._client[self._collection_name]
        return list(collection.find())

    def getById(self, id: int):
        pass

    def create(self, entity):
        pass

    def update(self, id: str, entity):
        pass

    def delete(self, id: str):
        pass
