from typing import Any

from src.domain.profile_brightdata import ProfileBrightDataDTO
from src.repositories.pipefy.mapping.card import CARD_START_FORM_MAPPING


def map_profile_bright_data_fields(profile: ProfileBrightDataDTO, pipe_id: str) -> dict:
    """Map profile bright data."""
    fields = CARD_START_FORM_MAPPING[pipe_id]["fields"]
    return [map_profile_bright_data_field(profile, field) for field in fields]


def map_profile_bright_data_field(profile: ProfileBrightDataDTO, field: dict[str, Any]) -> dict:
    """Map profile bright data field."""
    field_value = field["field_value"]

    if callable(field_value):
        field_value = field_value(profile)

    return {
        "field_id": field["field_id"],
        "field_value": field_value,
    }
