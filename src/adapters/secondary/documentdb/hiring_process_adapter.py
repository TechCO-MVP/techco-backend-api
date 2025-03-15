from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import HIRING_PROCESS_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.repositories.repository import IRepository
from src.domain.hiring_process import HiringProcessEntity
from src.repositories.document_db.client import DocumentDBClient
from src.errors.entity_not_found import EntityNotFound

logger = Logger("HiringProcessDBAdapter")


class HiringProcessDBAdapter(IRepository[HiringProcessEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = HIRING_PROCESS_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self, params: dict) -> list[HiringProcessEntity] | None:
        collection = self._client[self._collection_name]
        hiring_processes_data = collection.find({"business_id": params["business_id"]})
        hiring_processes_entities = []
        for hiring_process in hiring_processes_data:
            hiring_process["_id"] = str(hiring_process["_id"])

            hiring_processes_entities.append(
                from_dto_to_entity(HiringProcessEntity, hiring_process)
            )
        return hiring_processes_entities

    def getById(self, id: str) -> HiringProcessEntity:
        object_id = ObjectId(id)
        collection = self._client[self._collection_name]
        hiring_process = collection.find_one({"_id": object_id})

        if not hiring_process:
            raise EntityNotFound("HiringProcess", id)

        hiring_process["_id"] = str(hiring_process["_id"])

        return from_dto_to_entity(HiringProcessEntity, hiring_process)

    def getByCardId(self, card_id: str) -> HiringProcessEntity:
        collection = self._client[self._collection_name]
        hiring_process = collection.find_one({"card_id": card_id})

        if not hiring_process:
            raise EntityNotFound("HiringProcess", card_id)

        hiring_process["_id"] = str(hiring_process["_id"])
        return from_dto_to_entity(HiringProcessEntity, hiring_process)

    def create(self, entity: HiringProcessEntity) -> HiringProcessEntity:
        logger.info("Creating hiring process entity")
        logger.info(entity.to_dto(flat=True))

        hiring_process_data = entity.to_dto(flat=True)
        hiring_process_data.pop("_id", None)

        collection = self._client[self._collection_name]
        result = collection.insert_one(hiring_process_data, session=self._session)
        entity.id = str(result.inserted_id)

        return entity

    def update(self, id: str, entity: HiringProcessEntity) -> HiringProcessEntity:
        logger.info(f"Updating hiring process entity with id: {entity.id}")
        logger.info(entity.to_dto(flat=True))

        hiring_process_data = entity.to_dto(flat=True)
        hiring_process_data.pop("_id", None)
        hiring_process_data["updated_at"] = entity.updated_at

        collection = self._client[self._collection_name]
        collection.update_one(
            {"_id": ObjectId(id)}, {"$set": hiring_process_data}, session=self._session
        )

        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.delete_one({"_id": ObjectId(id)}, session=self._session)

    def getByPositionId(self, params: dict) -> list[HiringProcessEntity] | None:
        collection = self._client[self._collection_name]
        hiring_processes_data = collection.find({"position_id": params["position_id"]})
        hiring_processes_entities = []
        for hiring_process in hiring_processes_data:
            hiring_process["_id"] = str(hiring_process["_id"])

            hiring_processes_entities.append(
                from_dto_to_entity(HiringProcessEntity, hiring_process)
            )
        return hiring_processes_entities

    def getByLinkedinNumId(self, params: dict) -> HiringProcessEntity| None:
        collection = self._client[self._collection_name]
        hiring_process_data = collection.find_one(params)

        if not hiring_process_data:
            return None

        hiring_process_data["_id"] = str(hiring_process_data["_id"])
        hiring_processes_entities = from_dto_to_entity(HiringProcessEntity, hiring_process_data)
        
        return hiring_processes_entities
