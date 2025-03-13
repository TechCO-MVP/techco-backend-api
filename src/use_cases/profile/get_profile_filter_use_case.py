from typing import List

from src.domain.profile import PROCESS_TYPE, ProfileFilterProcessEntity
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository


def get_profile_filter_use_case(
    position_id: str, type: PROCESS_TYPE
) -> List[ProfileFilterProcessEntity]:
    """Get profile filter use case."""
    filter_params = {"position_id": position_id, "type": type}

    profile_filter_process_repository = ProfileFilterProcessRepository()
    profile_filter_process_entities = profile_filter_process_repository.getAll(filter_params)

    if not profile_filter_process_entities:
        raise EntityNotFound("Profile filter process", position_id)

    return profile_filter_process_entities
