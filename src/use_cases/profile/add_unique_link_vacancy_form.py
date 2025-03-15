import datetime
import jwt
import os
import re
import unicodedata

from src.domain.profile_brightdata import ProfileBrightDataDTO
from src.domain.profile import ProfileFilterProcessEntity
from src.adapters.secondary.documentdb.profile_filter_process_db_adapter import (
    ProfileFilterProcessDocumentDBAdapter,
)
from src.adapters.secondary.documentdb.business_db_adapter import BusinessDocumentDBAdapter


def add_unique_link_vacancy_form(event: ProfileFilterProcessEntity) -> ProfileFilterProcessEntity:
    """add unique link vacancy form for each profile use case."""

    event = add_links_form(event)

    profile_filter_process_repository = ProfileFilterProcessDocumentDBAdapter()
    response = profile_filter_process_repository.update(event.id, event)
    return response.to_dto(flat=True)


def add_links_form(event: ProfileFilterProcessEntity) -> ProfileFilterProcessEntity:
    """add links form for each profile use case."""
    business_repository = BusinessDocumentDBAdapter()
    for profile in event.props.profiles:
        token = encript_data(profile, event)
        vancancy_name = friendly_string(event.props.process_filters.role)
        business_entity = business_repository.getById(event.props.business_id)
        business_name = friendly_string(business_entity.props.name)
        profile.link_vacancy_form = (
            f"https://www.evoly.ofertas/{business_name}/{vancancy_name}?token={token}"
        )
    return event


def encript_data(profile: ProfileBrightDataDTO, event: ProfileFilterProcessEntity) -> str:
    """encript data with JWT"""

    payload = {
        "id": event.props.position_id,
        "business_id": event.props.business_id,
        "linkedin_num_id": profile.linkedin_num_id,
        "created_at": datetime.datetime.now().isoformat(),
        "exp": datetime.datetime.now() + datetime.timedelta(days=15),
    }

    token = jwt.encode(payload, os.getenv("PROFILE_FILTER_PROCESS_ARN"), algorithm="HS256")
    return token


def friendly_string(name: str) -> str:
    """
    Generate a friendly string by removing accents, replacing special characters,
    and replacing spaces and other special characters with hyphens
    """
    normalized_string = unicodedata.normalize("NFKD", name)
    ascii_string = normalized_string.encode("ascii", "ignore").decode("ascii")
    friendly_string = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_string)
    friendly_string = friendly_string.strip("-")
    friendly_string = friendly_string.lower()

    return friendly_string
