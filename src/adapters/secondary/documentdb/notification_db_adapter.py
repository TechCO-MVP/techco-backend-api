from datetime import datetime
from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import NOTIFICATION_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.notification import NotificationEntity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository

logger = Logger("NotificationDocumentDBAdapter")


class NotificationDocumentDBAdapter(IRepository[NotificationEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = NOTIFICATION_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)


    def getAll(self, params: dict) -> list[NotificationEntity] | None:
        collection = self._client[self._collection_name]
        notifications_data = collection.find(params)
        notifications_entities = []
        for notification in notifications_data:
            notification["_id"] = str(notification["_id"])
            notification["user_id"] = str(notification["user_id"])
            notification["business_id"] = str(notification["business_id"])
            notification["hiring_process_id"] = str(notification["hiring_process_id"])
            notifications_entities.append(from_dto_to_entity(NotificationEntity, notification))
        return notifications_entities

    def getById(self, id: str) -> NotificationEntity:
        object_id = ObjectId(id)
        collection = self._client[self._collection_name]
        notification = collection.find_one({"_id": object_id})

        if not notification:
            raise ValueError("Notification not found")

        notification["_id"] = str(notification["_id"])
        notification["user_id"] = str(notification["user_id"])

        return from_dto_to_entity(NotificationEntity, notification)

    def create(self, entity: NotificationEntity):
        try:
            notification_data = entity.to_dto(flat=True)
            notification_data.pop("_id", None)
            logger.info("Attempting to save notification for user: %s", notification_data["user_id"])

            collection = self._client[self._collection_name]
            
            result = collection.insert_one(notification_data, session=self._session)
            logger.info("notification successfully inserted with _id: %s", result.inserted_id)

            return {
                "message": "notification created successfully",
                "body": {"notification": {"_id": str(result.inserted_id)}},
            }
        except ValueError as ve:
            logger.error("Validation error while saving notification: %s", ve)
            raise ve
        except Exception as e:
            logger.error("Database error while saving notification: %s", e)
            raise Exception(f"Database error: {e}")

    def update(self, id: str, entity):
        collection = self._client[self._collection_name]
        dto = entity.to_dto(flat=True)
        dto.pop("_id", None)
        dto.pop("created_at", None)
        dto["updated_at"] = datetime.now().isoformat()

        collection.update_one({"_id": ObjectId(id)}, {"$set": dto})

        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.delete_one({"_id": id})
