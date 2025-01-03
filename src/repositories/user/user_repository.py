from aws_lambda_powertools import Logger

from src.adapters.secondary.documentdb.user_db_adapter import DocumentDBAdapter
from src.db.constants import USER_COLLECTION_NAME

logger = Logger()


class UserRepository:
    def __init__(self):
        self.adapter = DocumentDBAdapter()
        self.collection = self.adapter.get_collection(USER_COLLECTION_NAME)
        logger.info("UserRepository initialized and connected to the 'users' collection.")

    def save_user(self, user_data: dict) -> dict:
        """Save a user to the database."""

        try:
            logger.info("Attempting to save user with email: %s", user_data["email"])

            existing_user = self.collection.find_one({"email": user_data["email"]})

            if existing_user:
                logger.warning("User with email %s already exists.", user_data["email"])
                raise ValueError("A user with this email already exists.")

            result = self.collection.insert_one(user_data)
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
