from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, model_validator

from src.domain.base_entity import BaseEntity


class STATUS(str, Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class LEVEL(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WORK_MODE(str, Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRYD"
    ON_SITE = "ON_SITE"


class Skill(BaseModel):
    name: str
    required: bool


class Languages(BaseModel):
    name: str
    level: str


class Range(BaseModel):
    min: str
    max: str


class Salary(BaseModel):
    currency: str
    salary: Optional[str] = None
    salary_range: Optional[Range] = None


class Stakeholders(BaseModel):
    user_id: str
    can_edit: bool

class Phase(BaseModel):
    name: str
    thread_id: str
    status: STATUS
    data: dict


class PositionConfigurationDTO(BaseModel):

    user_id: str = Field(default="", alias="user_id")
    thread_id: str = Field(default="", alias="thread_id")
    status: STATUS = STATUS.DRAFT
    phases: Optional[List[Phase]] = Field(default=[])
    
    @model_validator(mode="before")
    def validate_and_convert_fields(cls, values):
        fields_to_validate = ["user_id"]
        for field in fields_to_validate:
            if field in values:
                if isinstance(values[field], ObjectId):
                    values[field] = str(values[field])
                elif not isinstance(values[field], str):
                    raise ValueError(f"Invalid {field} format. Must be a string or ObjectId.")
        return values


class PositionConfigurationEntity(BaseEntity[PositionConfigurationDTO]):
    pass
