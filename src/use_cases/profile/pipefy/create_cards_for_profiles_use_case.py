from aws_lambda_powertools import Logger

from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository
from src.repositories.document_db.position_repository import PositionRepository
from src.use_cases.profile.pipefy.create_pipe_configuration_open_position import (
    create_cards_for_profiles,
)

logger = Logger()


def create_cards_for_profiles_use_case(process_id: str, position_id: str, business_id: str) -> dict:
    """
    Use case for creating cards for profiles
    """
    logger.info("Creating cards for profiles")

    position_repository = PositionRepository()
    position = position_repository.getById(position_id)
    if not position:
        raise Exception("Position not found")

    profile_filter_process_repository = ProfileFilterProcessRepository()
    profile_filter_process = profile_filter_process_repository.getById(process_id)

    if profile_filter_process is None:
        raise Exception("Profile filter process not found")

    pipe_id = position.props.pipe_id
    profiles = profile_filter_process.props.profiles
    updated_profiles = create_cards_for_profiles(profiles, pipe_id, position_id, business_id)

    profile_filter_process.props.profiles = updated_profiles
    profile_filter_process_repository.update(profile_filter_process.id, profile_filter_process)

    logger.info("Cards created successfully")

    return profile_filter_process.to_dto(flat=True)
