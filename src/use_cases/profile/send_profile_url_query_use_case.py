from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.scraping.bright_data_dataset_repository import BrightDataDatasetRepository


def send_profile_url_query_use_case(
    profile_filter_entity: ProfileFilterProcessEntity,
) -> str:
    """
    Send profile URL query use case.
    This use case is responsible for sending a profile URL query to the
    scraping service and returning the snapshot ID.
    Args:
        profile_filter_entity (ProfileFilterProcessEntity): The profile filter entity to send.
    Returns:
        str: The snapshot ID of the profile filter process.
    """
    urls = profile_filter_entity.props.process_filters.url_profiles

    bright_data_dataset_repository = BrightDataDatasetRepository()
    snapshot_id = bright_data_dataset_repository.search_by_url(urls)

    return snapshot_id
