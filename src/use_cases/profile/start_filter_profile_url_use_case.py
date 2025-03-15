from src.domain.profile import (
    PROCESS_TYPE,
    ProfileFilterProcessQueryDTO,
)
from src.use_cases.profile.start_filter_profile_use_case import start_filter_profile_use_case


def start_filter_profile_url_use_case(
    profile_filter_process_query_dto: ProfileFilterProcessQueryDTO, user_email: str
) -> dict:
    """Start filter profiles by URL use case."""
    return start_filter_profile_use_case(
        profile_filter_process_query_dto, user_email, PROCESS_TYPE.PROFILES_URL_SEARCH
    )
