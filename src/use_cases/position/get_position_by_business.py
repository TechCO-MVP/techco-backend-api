from typing import Dict, List

from src.domain.position import PositionEntity
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.user_repository import UserRepository


def get_position_by_business_use_case(business_id: str) -> list[dict]:
    """get position by business use case."""
    position_repository = PositionRepository()
    hiring_repository = HiringProcessRepository()
    user_repository = UserRepository()
    positions = fetch_positions(business_id, position_repository)
    response = build_response(positions, hiring_repository, user_repository)

    return response


def fetch_positions(
    business_id: str, position_repository: PositionRepository
) -> List[PositionEntity]:
    """Fetch positions based on the business id."""

    return position_repository.getAll({"business_id": business_id})


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
