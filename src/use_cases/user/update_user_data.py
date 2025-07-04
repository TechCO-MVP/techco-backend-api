from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity
from src.domain.role import Role, BusinessRole
from aws_lambda_powertools import Logger


logger = Logger()


def put_user_data_use_case(user_data: dict) -> UserEntity:
    """put user data use case."""
    user_repository = UserRepository()
    user_data_db: UserEntity = user_repository.getByEmail(user_data["user_email"])

    if user_data.get("user_full_name"):
        user_data_db.props.full_name = user_data["user_full_name"]

    if user_data.get("company_position"):
        user_data_db.props.company_position = user_data["company_position"]

    if user_data.get("business_id") and user_data.get("user_role"):
        user_data_db = update_role_in_business_id(user_data_db, user_data)

    logger.info(f"Updating user data: {user_data_db}")
    return user_repository.update(user_data["user_id"], user_data_db)


def update_role_in_business_id(user_data_db: UserEntity, user_data: dict):
    """Update role in business id."""
    for index, business_role in enumerate(user_data_db.props.roles):
        if business_role.business_id == user_data["business_id"]:
            user_data_db.props.roles[index].role = Role(user_data["user_role"])
            break
        else:
            new_role = BusinessRole(
                role=Role(user_data["user_role"]),
                business_id=user_data["business_id"]
            )
            user_data_db.props.roles.append(new_role)
            break

    return user_data_db
