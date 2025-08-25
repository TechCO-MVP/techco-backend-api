from datetime import datetime
from typing import Any

from src.constants.index import DEFAULT_PIPE_TEMPLATE_ID
from src.domain.profile_evaluation import PROFILE_GROUP
from src.domain.profile_brightdata import ProfileBrightDataDTO, ExperienceProfile
from src.domain.profile import ProfileInfo
from src.domain.profile import PROCESS_TYPE

END_DATE_PRESENT_VALUES = ["Present", "Presente"]


def get_role_alignment(data: ProfileBrightDataDTO | ProfileInfo) -> str:
    alignments = {
        PROFILE_GROUP.HIGH.value: "Alta",
        PROFILE_GROUP.MID_HIGH.value: "Media - Alta",
        PROFILE_GROUP.MID.value: "Media",
        PROFILE_GROUP.LOW.value: "Baja",
    }
    return alignments.get(data.profile_evaluation.group)


def get_current_position(data: ProfileBrightDataDTO | ProfileInfo) -> ExperienceProfile:
    experience = data.experience or []
    current_experience = next(
        (exp for exp in experience if exp.end_date in END_DATE_PRESENT_VALUES), None
    )

    return current_experience


def get_position_info(data: ProfileBrightDataDTO | ProfileInfo) -> dict | None:
    if not data.position_info:
        return None

    position_info = {
        "recruiter_email": (
            data.position_info.get("recruiter_email", "") if data.position_info else ""
        ),
        "owner_email": data.position_info.get("owner_email", "") if data.position_info else "",
        "role": data.position_info.get("role", "") if data.position_info else "",
    }

    return position_info


def get_prop_from_position_info(data: ProfileBrightDataDTO | ProfileInfo, prop: str) -> Any:
    position_info = get_position_info(data)
    return position_info.get(prop, None) if position_info else None


def get_prop_from_current_position(data: ProfileBrightDataDTO | ProfileInfo, prop: str) -> Any:
    current_experience = get_current_position(data)
    return getattr(current_experience, prop) if current_experience else ""


def is_currently_employed(data: ProfileBrightDataDTO | ProfileInfo) -> str:
    current_experience = get_current_position(data)
    is_currently_employed = (
        current_experience.end_date in END_DATE_PRESENT_VALUES if current_experience else False
    )
    return "True" if is_currently_employed else "False"


def get_experience_end_date(data: ProfileBrightDataDTO | ProfileInfo) -> str:
    current_experience = get_current_position(data)
    if not current_experience:
        return None

    end_date = current_experience.end_date
    end_date = end_date if end_date != "Present" else None
    return end_date


def get_country_code(data: ProfileBrightDataDTO | ProfileInfo) -> str:
    ALLOWED_COUNTRY_CODES = ["CO", "PE", "MX"]
    if data.country_code not in ALLOWED_COUNTRY_CODES:
        return None
    return data.country_code


CARD_START_FORM_MAPPING = {
    DEFAULT_PIPE_TEMPLATE_ID: {
        "fields": [
            {
                "field_id": "305713420_334105217_avatar",
                "field_value": lambda data: data.avatar,
            },
            {
                "field_id": "305713420_334105217_candidatename",
                "field_value": lambda data: data.name,
            },
            {
                "field_id": "305713420_334105217_processstartday",
                "field_value": lambda _: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            },
            {"field_id": "305713420_334105217_candidatestatus", "field_value": "Activo"},
            {
                "field_id": "305713420_334105217_candidatecountry",
                "field_value": lambda data: get_country_code(data),
            },
            {
                "field_id": "305713420_334105217_candidatecity",
                "field_value": lambda data: data.city,
            },
            {
                "field_id": "305713420_334105217_corecompetencies",
                "field_value": lambda data: data.position,
            },
            {
                "field_id": "305713420_334105217_candidatebio",
                "field_value": lambda data: data.about,
            },
            {
                "field_id": "305713420_334105217_urllinkedin",
                "field_value": lambda data: data.url,
            },
            {
                "field_id": "305713420_334105217_rolealignment",
                "field_value": lambda data: get_role_alignment(data),
            },
            {
                "field_id": "305713420_334105217_fitfortheposition",
                "field_value": lambda data: data.profile_evaluation.description,
            },
            {
                "field_id": "305713420_334105217_aspectsnotdemonstratedbythecandidate",
                "field_value": lambda data: ", ".join(
                    data.profile_evaluation.vulnerabilities or []
                ),
            },
            {
                "field_id": "305713420_334105217_suggestions",
                "field_value": lambda data: ", ".join(data.profile_evaluation.recomendations or []),
            },
            {
                "field_id": "305713420_334105217_currentposition",
                "field_value": lambda data: get_prop_from_current_position(data, "title"),
            },
            {
                "field_id": "305713420_334105217_currentcompany",
                "field_value": lambda data: get_prop_from_current_position(data, "company"),
            },
            {
                "field_id": "305713420_334105217_timeinposition",
                "field_value": lambda data: get_prop_from_current_position(data, "duration"),
            },
            {
                "field_id": "305713420_334105217_currentlyemployed",
                "field_value": lambda data: is_currently_employed(data),
            },
            {
                "field_id": "305713420_334105217_dateworkbegan",
                "field_value": lambda data: get_prop_from_current_position(data, "start_date")
                or None,
            },
            {
                "field_id": "305713420_334105217_dateworkended",
                "field_value": lambda data: get_experience_end_date(data),
            },
            {
                "field_id": "305713420_334105217_urloftheinvitationtotheprocess",
                "field_value": lambda data: data.link_vacancy_form,
            },
            {
                "field_id": "305713420_334105217_candidateemail",
                "field_value": lambda data: data.email,
            },
            {
                "field_id": "305713420_334105217_candidatesource",
                "field_value": lambda data: (
                    "Talent Connect"
                    if data.source == PROCESS_TYPE.PROFILES_SEARCH.value
                    else "A través de la URL de la vacante"
                ),
            },
            {
                "field_id": "305713420_334105217_recruiteremail",
                "field_value": lambda data: get_prop_from_position_info(data, "recruiter_email"),
            },
            {
                "field_id": "305713420_334105217_jobvacancy",
                "field_value": lambda data: get_prop_from_position_info(data, "role"),
            },
            {
                "field_id": "305713420_334105217_owneremail",
                "field_value": lambda data: get_prop_from_position_info(data, "owner_email"),
            },
        ]
    }
}
