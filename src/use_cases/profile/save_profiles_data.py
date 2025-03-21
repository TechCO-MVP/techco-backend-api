from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.scraping.scraping_profile_filter_process import (
    ScrapingProfileFilterProcessRepository,
)
from src.constants.index import S3_RAW_PROFILE_DATA_IA_BUCKET_NAME
from src.repositories.s3.filter_profile import S3StorageRepository


def save_profiles_data_use_case(data: ProfileFilterProcessEntity) -> bool:
    """Save profiles in S3 use case."""

    scraping_profile_filter_process_repository = ScrapingProfileFilterProcessRepository()
    response = scraping_profile_filter_process_repository.get_data(
        data.props.process_filters.snapshot_id
    )

    storeage_repository = S3StorageRepository(S3_RAW_PROFILE_DATA_IA_BUCKET_NAME)
    storeage_repository.put(data.id, response)

    return response
