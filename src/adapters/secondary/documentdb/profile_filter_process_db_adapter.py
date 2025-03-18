from typing import List
from datetime import datetime

from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import PROFILE_FILTER_PROCESS_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository

logger = Logger("ProfileFilterProcessDocumentDBAdapter")


class ProfileFilterProcessDocumentDBAdapter(IRepository[ProfileFilterProcessEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = PROFILE_FILTER_PROCESS_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        # check if collection exists
        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self, filter_params: dict = None) -> List[ProfileFilterProcessEntity]:
        """
        Get all profile filter process entities from the database.
        """
        collection = self._client[self._collection_name]
        filter_params = filter_params or {}

        logger.info(f"Getting all profile filter process entities with filter: {filter_params}")

        result = []
        profile_filter_processes = list(collection.find(filter_params))
        if not profile_filter_processes:
            return []

        for profile_filter_process in profile_filter_processes:
            profile_filter_process["_id"] = str(profile_filter_process["_id"])
            result.append(from_dto_to_entity(ProfileFilterProcessEntity, profile_filter_process))

        return result

    def getById(self, id: str) -> ProfileFilterProcessEntity | None:
        logger.info(f"Getting profile filter process entity with id: {id}")

        collection = self._client[self._collection_name]
        result = collection.find_one({"_id": ObjectId(id)})

        if result is None:
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(ProfileFilterProcessEntity, result)

    def create(self, entity):
        logger.info("Creating profile filter process entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        profile_filter_process_data = entity.to_dto(flat=True)
        profile_filter_process_data.pop("_id", None)

        collection = self._client[self._collection_name]
        result = collection.insert_one(profile_filter_process_data, session=self._session)
        entity.id = str(result.inserted_id)

        logger.info(f"Entity created with id: {entity.id}")
        logger.info(result)
        return entity

    def update(self, id: str, entity):
        logger.info("Updating profile filter process entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        profile_filter_process_data = entity.to_dto(flat=True)
        profile_filter_process_data.pop("_id", None)
        profile_filter_process_data["updated_at"] = datetime.now().isoformat()

        collection = self._client[self._collection_name]
        result = collection.update_one(
            {"_id": ObjectId(id)}, {"$set": profile_filter_process_data}, session=self._session
        )

        logger.info(f"Update result: {result}")
        if result.matched_count == 0:
            logger.warning(f"No document found with id: {id}")
        elif result.modified_count == 0:
            logger.warning(f"Document with id: {id} was not modified")
        else:
            logger.info(f"Document with id: {id} was successfully updated")

        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"deleted_at": datetime.now()}}, session=self._session
        )
