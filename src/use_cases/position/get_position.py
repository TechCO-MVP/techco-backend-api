from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.user_repository import UserRepository
from src.domain.position import PositionEntity
from typing import List, Dict


def get_position_use_case(params: dict, user_email: str) -> list[dict]:
    """get position use case."""
    position_repository = PositionRepository()
    hiring_repository = HiringProcessRepository()
    user_repository = UserRepository()

    user_entity = user_repository.getByEmail(user_email)
    params["user_id"] = user_entity.id
    positions = fetch_positions(params, position_repository)
    response = build_response(positions, hiring_repository, user_repository)

    return response

def fetch_positions(params: dict, position_repository: PositionRepository) -> List[PositionEntity]:
    """Fetch positions based on the provided parameters."""
    if id := params.get("id"):
        return [position_repository.getById(id)]
    elif params["all"].lower() == "true":
        user_id = params["user_id"]
        query = {
            "business_id": params["business_id"],
            "$or": [
                {"owner_position_user_id": user_id},
                {"recruiter_user_id": user_id},
                {"responsible_users_ids": {"$elemMatch": {"user_id": user_id}}}
            ]
        }
        return position_repository.getAll(query)
    else:
        raise ValueError("Invalid values")
    
def build_response(positions: List[PositionEntity], hiring_repository: HiringProcessRepository, user_repository: UserRepository) -> List[Dict]:
    """Build the response data for the positions."""
    response = []

    for position in positions:
        data = position.to_dto(flat=True)
        data["total_hiring_processes"] = len(hiring_repository.getByPositionId({"position_id": position.id}))
        data["owner_position_user_name"] = user_repository.getById(data["owner_position_user_id"]).props.full_name
        data["recruiter_user_name"] = user_repository.getById(data["recruiter_user_id"]).props.full_name
        
        for index, stakeholder in enumerate(data["responsible_users"]):
            user = user_repository.getById(stakeholder["user_id"])
            data["responsible_users"][index]["user_name"] = user.props.full_name
        
        response.append(data)

    return response
