from aws_lambda_powertools import Logger
from pymongo.database import Database

from src.db.constants import USER_COLLECTION_NAME
from src.domain.user import UserEntity
from src.repositories.document_db.client import create_documentdb_client
from src.repositories.repository import IRepository

logger = Logger("UserDocumentDBAdapter")


class UserDocumentDBAdapter(IRepository[UserEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        self._collection_name = USER_COLLECTION_NAME
        self._client = create_documentdb_client()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self):
        collection = self._client[self._collection_name]
        return list(collection.find())

    def getById(self, id: str):
        collection = self._client[self._collection_name]
        return collection.find_one({"_id": id})

    def create(self, entity: UserEntity):
        try:
            user_data = entity.to_dto(flat=True)
            user_data.pop("_id", None)
            logger.info("Attempting to save user with email: %s", user_data["email"])

            collection = self._client[self._collection_name]
            existing_user = collection.find_one({"email": user_data["email"]})

            if existing_user:
                logger.warning("User with email %s already exists.", user_data["email"])
                raise ValueError("A user with this email already exists.")

            result = collection.insert_one(user_data)
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
