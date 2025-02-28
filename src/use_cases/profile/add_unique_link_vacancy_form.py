import datetime
import jwt
import os

from src.domain.profile_brightdata import ProfileBrightDataDTO
from src.domain.profile import ProfileFilterProcessEntity
from src.adapters.secondary.documentdb.profile_filter_process_db_adapter import (
    ProfileFilterProcessDocumentDBAdapter,
)


def add_unique_link_vacancy_form(event: ProfileFilterProcessEntity) -> ProfileFilterProcessEntity:
    """add unique link vacancy form for each profile use case."""

    event = add_links_form(event) 

    profile_filter_process_repository = ProfileFilterProcessDocumentDBAdapter()
    response = profile_filter_process_repository.update(event.id, event )
    return response.to_dto(flat=True)


def add_links_form(event: ProfileFilterProcessEntity) -> ProfileFilterProcessEntity:
    """add links form for each profile use case."""
    for profile in event.props.profiles:
        token = encript_data(profile, event)
        vancancy_name = (event.props.process_filters.role).replace(" ", "_")
        profile.link_vacancy_form = f"https://www.evoly.ofertas/{vancancy_name}?token={token}"
    return event


def encript_data(profile: ProfileBrightDataDTO, event: ProfileFilterProcessEntity) -> str:
    """encript data with JWT """

    payload = {
        "id": event.id,
        "business_id": event.props.business_id,
        "linkedin_id": profile.linkedin_num_id,
        "created_at": datetime.datetime.now().isoformat(),
        "exp": datetime.datetime.now() + datetime.timedelta(days=15)
    }

    token = jwt.encode(payload, os.getenv("PROFILE_FILTER_PROCESS_ARN"), algorithm="HS256")
    return token