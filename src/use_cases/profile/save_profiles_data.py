from src.constants.index import S3_RAW_PROFILE_DATA_IA_BUCKET_NAME
from src.domain.profile import PROCESS_TYPE, ProfileFilterProcessEntity
from src.repositories.s3.filter_profile import S3StorageRepository
from src.repositories.scraping.bright_data_dataset_repository import BrightDataDatasetRepository
from src.repositories.scraping.scraping_profile_filter_process import (
    ScrapingProfileFilterProcessRepository,
)


def save_profiles_data_use_case(data: ProfileFilterProcessEntity) -> bool:
    """Save profiles in S3 use case."""
    response = None

    if data.props.type == PROCESS_TYPE.PROFILES_URL_SEARCH:
        bright_data_dataset_repository = BrightDataDatasetRepository()
        response = bright_data_dataset_repository.get_snapshot_data(
            data.props.process_filters.snapshot_id
        )

    if data.props.type == PROCESS_TYPE.PROFILES_SEARCH:
        scraping_profile_filter_process_repository = ScrapingProfileFilterProcessRepository()
        response = scraping_profile_filter_process_repository.get_data(
            data.props.process_filters.snapshot_id
        )

    if response is None:
        raise NotImplementedError(
            f"Process type {data.props.type} not implemented for saving profiles data."
        )

    storeage_repository = S3StorageRepository(S3_RAW_PROFILE_DATA_IA_BUCKET_NAME)
    storeage_repository.put(data.id, response)

    return response
