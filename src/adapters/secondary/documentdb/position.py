from datetime import datetime

from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import POSITION_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.position import PositionEntity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository

logger = Logger("PositionDBAdapter")


class PositionDBAdapter(IRepository[PositionEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = POSITION_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        # check if collection exists
        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self, filter_params: dict = None):
        collection = self._client[self._collection_name]
        filter_params = filter_params or {}

        logger.info(f"Getting all position entities with filter: {filter_params}")

        result = []
        positions = list(collection.find(filter_params))
        if not positions:
            return []

        for position in positions:
            position["_id"] = str(position["_id"])
            result.append(from_dto_to_entity(PositionEntity, position))

        return result

    def getById(self, id: str) -> PositionEntity | None:
        logger.info(f"Getting position entity with id: {id}")

        collection = self._client[self._collection_name]
        result = collection.find_one({"_id": ObjectId(id)})

        if result is None:
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(PositionEntity, result)

    def create(self, entity):
        logger.info("Creating Position entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        position = entity.to_dto(flat=True)
        position.pop("_id", None)

        collection = self._client[self._collection_name]
        result = collection.insert_one(position, session=self._session)
        entity.id = str(result.inserted_id)

        logger.info(f"Entity created with id: {entity.id}")
        logger.info(result)
        return entity

    def update(self, id: str, entity):
        logger.info("Updating position entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        position = entity.to_dto(flat=True)
        position.pop("_id", None)
        position["updated_at"] = datetime.now().isoformat()

        collection = self._client[self._collection_name]
        result = collection.update_one(
            {"_id": ObjectId(id)}, {"$set": position}, session=self._session
        )

        logger.info(f"Entity updated with id: {id}")
        logger.info(result)
        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"deleted_at": datetime.now()}}, session=self._session
        )

    def getByPositionConfigirationId(self, id: str) -> PositionEntity | None:
        """Get a position entity by its position configuration id."""
        logger.info(f"Getting position entity with position configuration id: {id}")

        collection = self._client[self._collection_name]
        result = collection.find_one({"position_configuration_id": id})

        if result is None:
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(PositionEntity, result)
