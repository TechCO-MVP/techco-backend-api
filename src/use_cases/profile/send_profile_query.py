from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.scraping.scraping_profile_filter_process import ScrapingProfileFilterProcessRepository


def send_profile_query_use_case(filters: ProfileFilterProcessEntity) -> ProfileFilterProcessEntity:
    """Send profile query use case."""

    scraping_profile_filter_process_repository = ScrapingProfileFilterProcessRepository()
    response = scraping_profile_filter_process_repository.create(filters)
    return response
