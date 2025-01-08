from datetime import datetime

from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import BUSINESS_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.business import BusinessEntity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository

logger = Logger("BusinessDocumentDBAdapter")


class BusinessDocumentDBAdapter(IRepository[BusinessEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = BUSINESS_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

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
        result = collection.find_one({"_id": ObjectId(id)})

        if result is None:
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(BusinessEntity, result)

    def create(self, entity: BusinessEntity):
        logger.info("Creating business entity")
        logger.info(entity.to_dto(flat=True))

        business_data = entity.to_dto(flat=True)
        business_data.pop("_id", None)

        collection = self._client[self._collection_name]
        result = collection.insert_one(business_data, session=self._session)
        entity.id = str(result.inserted_id)
        return entity

    def update(self, id: str, entity):
        logger.info("Updating business entity")
        logger.info(entity.to_dto(flat=True))

        business_dto = entity.to_dto(flat=True)
        business_dto.pop("_id", None)

        collection = self._client[self._collection_name]
        collection.update_one({"_id": ObjectId(id)}, {"$set": business_dto}, session=self._session)
        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"deleted_at": datetime.now()}})
