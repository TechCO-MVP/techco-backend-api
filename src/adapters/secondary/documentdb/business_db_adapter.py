from pymongo.database import Database

from src.db.constants import BUSINESS_COLLECTION_NAME
from src.repositories.document_db.client import create_documentdb_client
from src.repositories.repository import IRepository
from src.domain.business import BusinessEntity


class BusinessDocumentDBAdapter(IRepository[BusinessEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        self._collection_name = BUSINESS_COLLECTION_NAME
        self._client = create_documentdb_client()

        # check if collection exists
        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self):
        collection = self._client[self._collection_name]
        return list(collection.find())

    def getById(self, id: str):
        collection = self._client[self._collection_name]
        return collection.find_one({"_id": id})

    def create(self, entity: BusinessEntity):
        collection = self._client[self._collection_name]
        collection.insert_one(entity.to_dto())
        return entity

    def update(self, id: str, entity):
        collection = self._client[self._collection_name]
        collection.update_one({"_id": id}, {"$set": entity.to_dto()})

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.delete_one({"_id": id})
