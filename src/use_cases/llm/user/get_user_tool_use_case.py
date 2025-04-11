from bson import ObjectId

from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.user_repository import UserRepository


def get_user_tool_llm_use_case(business_id: str) -> dict:
    """get user tool use case."""
    business_repository = BusinessRepository()

    business = business_repository.getById(business_id)
    if not business:
        raise Exception("Business not found")

    user_repository = UserRepository()
    filter_params = {
        "$or": [{"business_id": ObjectId(business_id)}, {"roles.business_id": business_id}]
    }

    users = user_repository.search(filter_params)
    if not users:
        raise Exception("Users not found")

    return [
        {
            "id": user.id,
            "full_name": user.props.full_name,
        }
        for user in users
    ]
