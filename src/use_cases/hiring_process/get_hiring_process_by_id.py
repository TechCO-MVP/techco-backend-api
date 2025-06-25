from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.user_repository import UserRepository
from typing import Dict, Any


def get_hiring_process_by_id_use_case(params: dict) -> list[dict]:
    """get position by token use case."""
    hiring_process_id = params.get("hiring_process_id")

    hiring_repository = HiringProcessRepository()
    position_repository = PositionRepository()
    user_repository = UserRepository()

    hiring = hiring_repository.getById(hiring_process_id)
    position = position_repository.getById(hiring.props.position_id)
    hiring_data = {
        "position_country": position.props.country_code,
        "position_city": position.props.city,
        "position_status": position.props.status,
    }
    recruiter_id = position.props.recruiter_user_id or None
    if recruiter_id:
        data_recruiter = get_user_data(recruiter_id, user_repository, "recruiter")
    else:
        data_recruiter = {}

    owner_id = position.props.owner_position_user_id
    data_owner = get_user_data(owner_id, user_repository, "owner")

    stakeholders = position.props.responsible_users
    data_stakeholders = [get_stake_holder_data(stakeholder, user_repository) for stakeholder in stakeholders]

    response = build_response(hiring_data, data_recruiter, data_owner, data_stakeholders)

    return response

def get_user_data(user_id: str, user_repository: UserRepository, user_type: str) -> dict:
    """Get the data of the user."""
    user = user_repository.getById(user_id)

    return {
        f"{user_type}_id": user.id,
        f"{user_type}_name": user.props.full_name,
    }

def get_stake_holder_data(stakeholder: str, user_repository: UserRepository) -> dict:
    """Get the data of the stakeholder."""
    data_stakeholder = get_user_data(stakeholder.user_id, user_repository, "stakeholder")
    data_stakeholder["can_edit"] = stakeholder.can_edit

    return data_stakeholder

def build_response(hiring_data: dict, data_recruiter: dict, data_owner: dict, data_stakeholders: dict) -> Dict[str, Any]:
    """Build the response data for the hiring data."""   
    response = {
        **hiring_data,
        **data_recruiter,
        **data_owner,
        "stakeholders": data_stakeholders
    }
    return response
