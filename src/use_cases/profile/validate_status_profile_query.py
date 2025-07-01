from src.domain.profile import PROCESS_TYPE
from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.scraping.scraping_profile_filter_process import (
    ScrapingProfileFilterProcessRepository,
)
from src.repositories.scraping.bright_data_dataset_repository import BrightDataDatasetRepository


def validate_status_profile_query_use_case(data: ProfileFilterProcessEntity) -> bool:
    """Send profile query use case."""

    if data.props.type == PROCESS_TYPE.PROFILES_URL_SEARCH:
        bright_data_dataset_repository = BrightDataDatasetRepository()
        response = bright_data_dataset_repository.get_snapshot_status(
            data.props.process_filters.snapshot_id
        )

        return response

    if data.props.type == PROCESS_TYPE.PROFILES_SEARCH:
        scraping_profile_filter_process_repository = ScrapingProfileFilterProcessRepository()

        response = scraping_profile_filter_process_repository.get_status(
            data.props.process_filters.snapshot_id
        )

        return response

    raise NotImplementedError(f"Process type {data.props.type} not valid.")
