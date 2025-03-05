from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.user_repository import UserRepository
from src.domain.position import PositionEntity


def get_position_use_case(params: dict) -> list[dict]:
    """get position use case."""
    position_repository = PositionRepository()

    if id := params.get("id"):
        positions = [position_repository.getById(id)]
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
        positions = position_repository.getAll(query)
    else:
        raise ValueError("Invalid values")
    
    hiring_repository = HiringProcessRepository()

    position_fields = ("owner_position_user_id", "recruiter_user_id", "responsible_users", "role", "hiring_priority")
    hiring_fields = ("id", "card_id", "status")
    response = []
    for position in positions:
        data = {""}
        hiring_process = hiring_repository.getAll({"position_id": position.id})


