from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.user_repository import UserRepository
from src.domain.position import PositionEntity
from typing import List, Dict


def get_position_use_case(params: dict) -> list[dict]:
    """get position use case."""
    position_repository = PositionRepository()
    hiring_repository = HiringProcessRepository()
    user_repository = UserRepository()

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
    position_fields = ("owner_position_user_id", "recruiter_user_id", "responsible_users", "role", "hiring_priority")
    response = []
    for position in positions:
        data = {}
        list_stakeholders = []
        data["hiring_processes"] = fetch_hiring_processes(position.id, hiring_repository)

        for field in position_fields:
            data[field] = getattr(position.props, field)
            if field == "owner_position_user_id" or field == "recruiter_user_id":
                user = user_repository.getById(data[field])
                data[field[:-3]] = {"name": user.props.full_name, "id": user.id}
                data.pop(field)
            
            if field == "responsible_users":
                for stakeholder in data[field]:
                    user = user_repository.getById(stakeholder.user_id)
                    data_stakeholder = {"name": user.props.full_name, "id": user.id, "can_edit": stakeholder.can_edit}
                    list_stakeholders.append(data_stakeholder)
                data[field] = list_stakeholders
        response.append(data)

    return response

def fetch_hiring_processes(position_id: str, hiring_repository: HiringProcessRepository) -> List[Dict]:
    """Fetch hiring processes for a given position."""
    list_hiring_processes = []
    hiring_fields = ("card_id", "status")
    hiring_processes = hiring_repository.getByPositionId({"position_id": position_id})
    
    for hiring_process in hiring_processes:
        hiring_data = {field: getattr(hiring_process.props, field) for field in hiring_fields}
        hiring_data["id"] = hiring_process.id
        list_hiring_processes.append(hiring_data)
    
    return list_hiring_processes

def fetch_position_fields(position: PositionEntity, user_repository: UserRepository) -> Dict:
    """Fetch and format position fields."""
    data = {}
    list_stakeholders = []
    position_fields = ("owner_position_user_id", "recruiter_user_id", "responsible_users", "role", "hiring_priority")

    for field in position_fields:
        field_value = getattr(position.props, field)
        if field in ["owner_position_user_id", "recruiter_user_id"]:
            user = user_repository.getById(field_value)
            data[field[:-3]] = {"name": user.props.full_name, "id": user.id}
        elif field == "responsible_users":
            for stakeholder in field_value:
                user = user_repository.getById(stakeholder.user_id)
                data_stakeholder = {"name": user.props.full_name, "id": user.id, "can_edit": stakeholder.can_edit}
                list_stakeholders.append(data_stakeholder)
            data[field] = list_stakeholders
        else:
            data[field] = field_value

    return data
