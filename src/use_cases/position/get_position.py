from src.repositories.document_db.position_repository import PositionRepository
from src.domain.position import PositionEntity


def get_position_use_case(params: dict) -> PositionEntity:
    """get position use case."""
    position_repository = PositionRepository()

    if id := params.get("id"):
        return position_repository.getById(id)
    elif params["all"].lower() == "true":
        user_id = params["user_id"]
        query = {
            "business_id": params["business_id"],
            "$or": [
                {"owner_position_user_id": user_id},
                {"recruiter_user_id": user_id},
                {"responsible_users": {"$elemMatch": {"user_id": user_id}}}
            ]
        }
        return position_repository.getAll(query)
    else:
        raise ValueError("Invalid values")
