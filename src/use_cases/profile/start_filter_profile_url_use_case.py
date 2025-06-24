from typing import List

from src.domain.profile import PROCESS_TYPE, ProfileFilterProcessQueryDTO
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity
from src.use_cases.profile.start_filter_profile_use_case import start_filter_profile_use_case


def start_filter_profile_url_use_case(
    position_id: str, business_id: str, url_profiles: List[str]
) -> dict:
    """Start filter profiles by URL use case."""

    position_repository = PositionRepository()
    position = position_repository.getById(position_id)
    user_repository = UserRepository()
    user_entity: UserEntity = user_repository.getById(position.props.owner_position_user_id)
    user_email = user_entity.props.email

    if not position:
        raise EntityNotFound("Position", position_id)

    profile_filter_process_query_dto = ProfileFilterProcessQueryDTO(
        role=position.props.role,
        seniority=position.props.seniority,
        country_code=position.props.country_code,
        city=position.props.city,
        description=position.props.description,
        responsabilities=position.props.responsabilities,
        skills=position.props.skills,
        business_id=business_id,
        position_id=position_id,
        url_profiles=url_profiles,
    )

    return start_filter_profile_use_case(
        profile_filter_process_query_dto, user_email, PROCESS_TYPE.PROFILES_URL_SEARCH
    )
