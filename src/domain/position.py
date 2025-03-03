from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from src.domain.base_entity import BaseEntity


class PROCESS_STATUS(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class LEVEL(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WORK_MODE(str, Enum):
    REMOTE = "Remote"
    HYBRID  = "Hybrid "
    ON_SITE = "On-site"

class Skill(BaseModel):
    name: str
    required: bool

class Languages(BaseModel):
    name: str
    level: str

class Salary(BaseModel):
    currency: str
    salary: str
    salara_range: str


class PositionDTO(BaseModel):
    business_id: str = Field(default="", alias="business_id")
    role: str
    seniority: str
    country_code: str = Field(..., min_length=2, max_length=2)
    city: str
    description: str
    responsabilities: List[str] = Field(..., min_length=1)
    skills: List[Skill] = Field(..., min_length=1)
    languages: List[Languages] = Field(..., min_length=1)
    benefits: Optional[List[str]] = Field(default_factory=list)
    salary_range: Optional[Salary]
    hiring_priority: LEVEL
    work_mode: WORK_MODE


    @field_validator("business_id", mode="before")
    def validate_and_convert_business_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v

        raise ValueError("Invalid business_id format. Must be a string or ObjectId.")


class PositionEntity(BaseEntity[PositionDTO]):
    pass
