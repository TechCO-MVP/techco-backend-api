from typing import Dict, List

from src.domain.position import PositionEntity
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity
from src.domain.role import Role

from src.utils.index import get_role_business


def get_position_use_case(params: dict, user_email: str) -> list[dict]:
    """get position use case."""
    position_repository = PositionRepository()
    hiring_repository = HiringProcessRepository()
    user_repository = UserRepository()

    user_entity = user_repository.getByEmail(user_email)
    params["user_id"] = user_entity.id
    positions = fetch_positions(params, position_repository, user_entity)
    response = build_response(positions, hiring_repository, user_repository)

    return response


def fetch_positions(
    params: dict, position_repository: PositionRepository, user_entity: UserEntity
) -> List[PositionEntity]:
    """Fetch positions based on the provided parameters."""
    if id := params.get("id"):
        return [position_repository.getById(id)]
    elif params["all"].lower() == "true":
        business_id = params["business_id"]
        role = get_role_business(user_entity, business_id)

        if not role:
            raise ValueError("Role not found for the given business id")

        if role.role in [Role.SUPER_ADMIN.value, Role.BUSINESS_ADMIN.value]:
            return fetch_position_for_admin(params, position_repository)

        user_id = params["user_id"]
        query = {
            "business_id": params["business_id"],
            "$or": [
                {"owner_position_user_id": user_id},
                {"recruiter_user_id": user_id},
                {"responsible_users_ids": {"$elemMatch": {"user_id": user_id}}},
            ],
        }
        return position_repository.getAll(query)
    else:
        raise ValueError("Invalid values")


def build_response(
    positions: List[PositionEntity],
    hiring_repository: HiringProcessRepository,
    user_repository: UserRepository,
) -> List[Dict]:
    """Build the response data for the positions."""
    response = []

    for position in positions:
        data = position.to_dto(flat=True)
        hiring_processes = hiring_repository.getByPositionId({"position_id": position.id})
        data["hiring_processes"] = [
            hiring_process.to_dto(flat=True) for hiring_process in hiring_processes
        ]
        data["total_hiring_processes"] = len(hiring_processes)
        data["owner_position_user_name"] = user_repository.getById(
            data["owner_position_user_id"]
        ).props.full_name
        data["recruiter_user_name"] = user_repository.getById(
            data["recruiter_user_id"]
        ).props.full_name

        for index, stakeholder in enumerate(data["responsible_users"]):
            user = user_repository.getById(stakeholder["user_id"])
            data["responsible_users"][index]["user_name"] = user.props.full_name

        response.append(data)

    return response


def fetch_position_for_admin(
    params: dict, position_repository: PositionRepository
) -> List[PositionEntity]:
    """Fetch positions for admin based on the provided parameters."""

    query = {"business_id": params["business_id"]}
    return position_repository.getAll(query)
