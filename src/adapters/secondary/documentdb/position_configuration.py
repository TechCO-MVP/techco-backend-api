from datetime import datetime

from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import POSITION_CONFIGURATION_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.position_configuration import PositionConfigurationEntity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository

logger = Logger("PositionConfigurationDBAdapter")


class PositionConfigurationDBAdapter(IRepository[PositionConfigurationEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = POSITION_CONFIGURATION_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        # check if collection exists
        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self, filter_params: dict = None) -> list[PositionConfigurationEntity]:
        """Get all position_configuration entities from the database."""
        collection = self._client[self._collection_name]
        filter_params = filter_params or {}

        logger.info(f"Getting all position_configuration entities with filter: {filter_params}")

        result = []
        positions_configuration = list(collection.find(filter_params).sort("created_at", -1))
        if not positions_configuration:
            return []

        for position in positions_configuration:
            position["_id"] = str(position["_id"])
            result.append(from_dto_to_entity(PositionConfigurationEntity, position))

        return result

    def getById(self, id: str) -> PositionConfigurationEntity | None:
        logger.info(f"Getting position configuration entity with id: {id}")

        collection = self._client[self._collection_name]
        result = collection.find_one({"_id": ObjectId(id)})

        if result is None:
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(PositionConfigurationEntity, result)

    def create(self, entity: PositionConfigurationEntity) -> PositionConfigurationEntity:
        """Create a new position_configuration entity in the database."""
        logger.info("Creating Position configuration entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        position_configuration = entity.to_dto(flat=True)
        position_configuration.pop("_id", None)

        collection = self._client[self._collection_name]
        result = collection.insert_one(position_configuration, session=self._session)
        entity.id = str(result.inserted_id)

        logger.info(f"Entity created with id: {entity.id}")
        logger.info(result)
        return entity

    def update(self, id: str, entity: PositionConfigurationEntity) -> PositionConfigurationEntity:
        logger.info("Updating position colnfiguration entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        position_configuration = entity.to_dto(flat=True)
        position_configuration.pop("_id", None)
        position_configuration["updated_at"] = datetime.now().isoformat()

        collection = self._client[self._collection_name]
        result = collection.update_one(
            {"_id": ObjectId(id)}, {"$set": position_configuration}, session=self._session
        )

        logger.info(f"Entity updated with id: {id}")
        logger.info(result)
        return entity

    def delete(self, id: str) -> None:
        """Delete a position_configuration entity from the database."""
        logger.info(f"Deleting position_configuration entity with id: {id}")
        collection = self._client[self._collection_name]
        collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"deleted_at": datetime.now()}}, session=self._session
        )
