
from src.domain.profile import (
    PROCESS_STATUS,
    ProfileFilterProcessDTO,
    ProfileFilterProcessEntity,
    ProfileFilterProcessQueryDTO,
)
from src.repositories.scraping.scraping_profile_filter_process import ScrapingProfileFilterProcessRepository


def send_profile_query_use_case(filters: ProfileFilterProcessDTO) -> dict:
    """Send profile query use case."""

    scraping_profile_filter_process_repository = ScrapingProfileFilterProcessRepository()
    filters_entity = create_profile_filter_process_entity(filters, filters.user_id)
    response = scraping_profile_filter_process_repository.create(filters_entity)
    return response.props.process_filters.snapshot_id

def create_profile_filter_process_entity(
    profile_filter_process_query_dto: ProfileFilterProcessQueryDTO, user_id: str
) -> ProfileFilterProcessEntity:
    profile_filter_process_dto = ProfileFilterProcessDTO(
        status=PROCESS_STATUS.IN_PROGRESS,
        user_id=user_id,
        position_id=profile_filter_process_dto.position_id,
        business_id=profile_filter_process_dto.business_id,
        process_filters=profile_filter_process_query_dto,
    )

    return ProfileFilterProcessEntity(props=profile_filter_process_dto)