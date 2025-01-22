from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity
from aws_lambda_powertools import Logger


logger = Logger()


def get_user_by_mail_use_case(user_email: str) -> UserEntity:
    """put user data use case."""
    user_repository = UserRepository()
    return user_repository.getByEmail(user_email)
