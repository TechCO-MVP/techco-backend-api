from enum import Enum
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from src.domain.base_entity import BaseEntity
from src.domain.user import UserDTO


class PROCESS_STATUS(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProfileFilterProcessQueryDTO(BaseModel):
    role: str
    seniority: str
    country_code: str = Field(..., min_length=2, max_length=3)
    city: str
    description: str
    responsibilities: List[str] = Field(..., min_length=1)
    skills: List[str] = Field(..., min_length=1)
    business_id: str = Field(default="", alias="business_id")
    position_id: str = Field(default="", alias="position_id")


class ProfileFilterProcessDTO(BaseModel):
    status: PROCESS_STATUS = PROCESS_STATUS.PENDING
    user: UserDTO
    position_id: str = Field(default="", alias="position_id")
    business_id: str = Field(default="", alias="business_id")
    process_filters: ProfileFilterProcessQueryDTO

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
