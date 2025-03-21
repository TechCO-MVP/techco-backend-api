import re
from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from src.domain.base_entity import BaseEntity
from src.domain.profile_brightdata import ProfileBrightDataDTO


class PROCESS_STATUS(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PROCESS_TYPE(str, Enum):
    PROFILES_SEARCH = "profiles_search"
    PROFILES_URL_SEARCH = "profiles_url_search"


class Skill(BaseModel):
    name: str
    required: bool


class ProfileFilterProcessQueryDTO(BaseModel):
    role: str
    seniority: str
    country_code: str = Field(..., min_length=2, max_length=3)
    city: str
    description: str
    responsabilities: List[str] = Field(..., min_length=1)
    skills: List[Skill] = Field(..., min_length=1)
    business_id: str = Field(default="", alias="business_id")
    position_id: str = Field(default="", alias="position_id")
    snapshot_id: Optional[str] = ""
    url_profiles: Optional[List[str]] = []

    @field_validator("url_profiles", mode="before")
    def validate_url_profiles(cls, v):
        if not v:
            return v
        for url in v:
            pattern = re.compile(r"^https://www\.linkedin\.com/in/.*$")
            if not pattern.match(url):
                raise ValueError(f"Invalid URL format: {url}")
        return v


class ProfileFilterProcessDTO(BaseModel):
    status: PROCESS_STATUS = PROCESS_STATUS.PENDING
    type: PROCESS_TYPE = PROCESS_TYPE.PROFILES_SEARCH
    execution_arn: Optional[str] = None
    user_id: str
    position_id: str = Field(default="", alias="position_id")
    business_id: str = Field(default="", alias="business_id")
    process_filters: ProfileFilterProcessQueryDTO
    profiles: Optional[List[ProfileBrightDataDTO]] = []

    @field_validator("position_id", mode="before")
    def validate_and_convert_position_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v

        raise ValueError("Invalid position_id format. Must be a string or ObjectId.")

    @field_validator("business_id", mode="before")
    def validate_and_convert_business_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v

        raise ValueError("Invalid business_id format. Must be a string or ObjectId.")


class ProfileFilterProcessEntity(BaseEntity[ProfileFilterProcessDTO]):
    pass
