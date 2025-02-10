
from src.domain.profile import ProfileFilterProcessDTO
from src.repositories.scraping.scraping_profile_filter_process import ScrapingProfileFilterProcessRepository


def validate_status_profile_query_use_case(data: ProfileFilterProcessDTO) -> bool:
    """Send profile query use case."""

    scraping_profile_filter_process_repository = ScrapingProfileFilterProcessRepository()

    response = scraping_profile_filter_process_repository.get_status(data.snapshot_id)
    
    return response
