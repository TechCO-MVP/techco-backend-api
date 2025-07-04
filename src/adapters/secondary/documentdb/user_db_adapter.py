from datetime import datetime
from aws_lambda_powertools import Logger
from bson import ObjectId
from pymongo.database import Database

from src.db.constants import BUSINESS_COLLECTION_NAME, USER_COLLECTION_NAME
from src.domain.base_entity import from_dto_to_entity
from src.domain.role import Role
from src.domain.user import UserEntity
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.repository import IRepository
from src.errors.entity_not_found import EntityNotFound

logger = Logger("UserDocumentDBAdapter")


class UserDocumentDBAdapter(IRepository[UserEntity]):

    _client: Database

    def __init__(self):
        super().__init__()
        document_db_client = DocumentDBClient()
        self._collection_name = USER_COLLECTION_NAME
        self._business_collection_name = BUSINESS_COLLECTION_NAME
        self._client = document_db_client.create_documentdb_database_client()
        self._session = document_db_client.get_session()

        if self._collection_name not in self._client.list_collection_names():
            self._client.create_collection(self._collection_name)

        indexes = self._client[self._collection_name].index_information()
        if "email" not in indexes:
            self._client[self._collection_name].create_index("email", unique=True)

    def getAll(self, params: dict) -> list[UserEntity] | None:
        logger.info(f"Getting all user entities with filter: {params}")

        collection = self._client[self._collection_name]
        query = {"roles": {"$elemMatch": {"business_id": params["business_id"]}}}

        if "exclude_business_id" in params:
            query["roles.business_id"] = {"$ne": params["exclude_business_id"]}

        users_data = collection.find(query)
        users_entities = []
        for user in users_data:
            user["_id"] = str(user["_id"])
            user["business_id"] = str(user["business_id"])
            users_entities.append(from_dto_to_entity(UserEntity, user))
        return users_entities

    def search(self, params: dict) -> list[UserEntity] | None:
        logger.info(f"Searching user entities with filter: {params}")

        collection = self._client[self._collection_name]
        users_data = collection.find(params)
        users_entities = []
        for user in users_data:
            user["_id"] = str(user["_id"])
            user["business_id"] = str(user["business_id"])
            users_entities.append(from_dto_to_entity(UserEntity, user))

        return users_entities

    def getByEmail(self, email: str) -> UserEntity:
        logger.info(f"Getting user entity with email: {email}")
        collection = self._client[self._collection_name]
        result = collection.find_one({"email": email})

        if not result:
            raise EntityNotFound("User", email)

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(UserEntity, result)

    def getById(self, id: str) -> UserEntity:
        object_id = ObjectId(id)
        collection = self._client[self._collection_name]
        user = collection.find_one({"_id": object_id})

        if not user:
            raise ValueError("User not found")

        user["_id"] = str(user["_id"])
        user["business_id"] = str(user["business_id"])

        return from_dto_to_entity(UserEntity, user)

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
            exists_business = business_collection.find_one(
                {"_id": business_object_id}, session=self._session
            )

            if not exists_business:
                logger.warning("business with id %s not exists.", user_data["business_id"])
                raise ValueError("A business_id not exists.")

            user_data["business_id"] = business_object_id
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
        dto = entity.to_dto(flat=True)
        dto.pop("_id", None)
        dto.pop("created_at", None)
        dto["business_id"] = ObjectId(dto["business_id"])
        dto["updated_at"] = datetime.now().isoformat()

        collection.update_one({"_id": ObjectId(id)}, {"$set": dto})

        return entity

    def delete(self, id: str):
        collection = self._client[self._collection_name]
        collection.delete_one({"_id": id})

    def get_admin_user_by_business_id(self, business_id: str) -> UserEntity:
        """Get admin user by business_id."""
        logger.info(f"Getting admin user by business_id: {business_id}")
        collection = self._client[self._collection_name]
        result = collection.find_one(
            {"roles.business_id": business_id, "roles.role": Role.SUPER_ADMIN.value}
        )

        if not result:
            logger.warning("User with business_id %s not found.", business_id)
            return None

        result["_id"] = str(result["_id"])
        return from_dto_to_entity(UserEntity, result)
