from aws_lambda_powertools import Logger
from bson.objectid import ObjectId
from pymongo.database import Database

from src.db.constants import BUSINESS_COLLECTION_NAME, USER_COLLECTION_NAME
from src.domain.user import UserEntity, filter_user_dto_fields
from src.repositories.document_db.client import create_documentdb_client
from src.repositories.repository import IRepository

logger = Logger("UserDocumentDBAdapter")


class UserDocumentDBAdapter(IRepository[UserEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        self._collection_name = USER_COLLECTION_NAME
        self._business_collection_name = BUSINESS_COLLECTION_NAME
        self._client = create_documentdb_client()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

    def getAll(self, business_id: str) -> dict:
        collection = self._client[self._collection_name]
        users_data = list(collection.find({"business_id": business_id}))
        message = "Users found successfully"

        if not users_data:
            message = "No users found"

        return {"message": message, "body": [filter_user_dto_fields(user) for user in users_data]}

    def getById(self, id: str, business_id: str) -> dict:
        object_id = ObjectId(id)
        collection = self._client[self._collection_name]
        user = collection.find_one({"_id": object_id, "business_id": business_id})

        if not user:
            raise ValueError("User not found")

        user_data = filter_user_dto_fields(user)
        message = "User found successfully"

        return {"message": message, "body": [user_data]}

    def create(self, entity: UserEntity):
        try:
            user_data = entity.to_dto(flat=True)
            user_data.pop("_id", None)
            logger.info("Attempting to save user with email: %s", user_data["email"])

            collection = self._client[self._collection_name]
            exists_user = collection.find_one({"email": user_data["email"]})

            if exists_user:
                logger.warning("User with email %s already exists.", user_data["email"])
                raise ValueError("A user with this email already exists.")

            business_collection = self._client[self._business_collection_name]
            business_object_id = ObjectId(user_data["business_id"])
            exists_business = business_collection.find_one({"_id": business_object_id})

            if not exists_business:
                logger.warning("business with id %s not exists.", user_data["business_id"])
                raise ValueError("A business_id not exists.")

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
