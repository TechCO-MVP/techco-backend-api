from aws_lambda_powertools import Logger
from pymongo.database import Database

from src.db.constants import BUSINESS_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.business import BusinessEntity
from src.repositories.document_db.client import create_documentdb_client
from src.repositories.repository import IRepository

logger = Logger("BusinessDocumentDBAdapter")


class BusinessDocumentDBAdapter(IRepository[BusinessEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        self._collection_name = BUSINESS_COLLECTION_NAME
        self._client = create_documentdb_client()

        # check if collection exists
        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self, filter_params: dict = None):
        collection = self._client[self._collection_name]
        filter_params = filter_params or {}
        return list(collection.find(filter_params))

    def getById(self, id: str) -> BusinessEntity | None:
        logger.info(f"Getting business entity with id: {id}")

        collection = self._client[self._collection_name]
        result = collection.find_one({"_id": id})

        if result is None:
            return None

        return from_dto_to_entity(BusinessEntity, result)

    def create(self, entity: BusinessEntity):
        logger.info("Creating business entity")
        logger.info(entity.to_dto(flat=True))

        collection = self._client[self._collection_name]
        result = collection.insert_one(entity.to_dto(flat=True))
        entity.id = str(result.inserted_id)
        return entity

    def update(self, id: str, entity):
        logger.info("Updating business entity")
        logger.info(entity.to_dto(flat=True))

        collection = self._client[self._collection_name]
        collection.update_one({"_id": id}, {"$set": entity.to_dto(flat=True)})
        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.delete_one({"_id": id})
