from bson import ObjectId
from aws_lambda_powertools import Logger
from pymongo.database import Database

from src.db.constants import USER_COLLECTION_NAME
from src.domain.user import UserEntity
from src.domain.base_entity import from_dto_to_entity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository

logger = Logger("UserDocumentDBAdapter")


class UserDocumentDBAdapter(IRepository[UserEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = USER_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self):
        collection = self._client[self._collection_name]
        return list(collection.find())

    def getById(self, id: str):
        collection = self._client[self._collection_name]
        return collection.find_one({"_id": id})

    def getByEmail(self, email: str) -> UserEntity | None:
        logger.info(f"Getting user entity with email: {email}")

        collection = self._client[self._collection_name]
        result = collection.find_one({"email": email})

        if result is None:
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(UserEntity, result)

    def create(self, entity: UserEntity):
        try:
            user_data = entity.to_dto(flat=True)
            user_data.pop("_id", None)
            user_data["business_id"] = ObjectId(user_data["business_id"])
            logger.info("Attempting to save user with email: %s", user_data["email"])

            collection = self._client[self._collection_name]
            existing_user = collection.find_one({"email": user_data["email"]})

            if existing_user:
                logger.warning("User with email %s already exists.", user_data["email"])
                raise ValueError("A user with this email already exists.")

            result = collection.insert_one(user_data, session=self._session)
            logger.info("User successfully inserted with _id: %s", result.inserted_id)

            return {
                "message": "User created successfully",
                "body": {"user": {"_id": str(result.inserted_id)}},
            }
        except ValueError as ve:
            logger.error("Validation error while saving user: %s", ve)
            raise ve
        except Exception as e:
            logger.error("Database error while saving user: %s", e)
            raise Exception(f"Database error: {e}")

    def update(self, id: str, entity):
        collection = self._client[self._collection_name]
        collection.update_one({"_id": id}, {"$set": entity.to_dto()})

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.delete_one({"_id": id})
