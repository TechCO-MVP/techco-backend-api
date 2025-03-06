from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError

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

class PositionStakeholders(BaseModel):
    user_id: str
    can_edit: bool

class PositionDTO(BaseModel):
    business_id: str = Field(default="", alias="business_id")
    owner_position_user_id: str
    recruiter_user_id: str
    responsible_users: List[PositionStakeholders] = Field(default_factory=list)
    role: str
    seniority: str
    country_code: str = Field(..., min_length=2, max_length=2)
    city: str
    description: str
    responsabilities: List[str] = Field(..., min_length=1)
    skills: List[Skill] = Field(..., min_length=1)
    languages: List[Languages] = Field(..., min_length=1)
    hiring_priority: LEVEL
    work_mode: WORK_MODE
    benefits: Optional[List[str]] = Field(default_factory=list)
    salary_range: Optional[Salary] = Field(default_factory=list)


    @model_validator(mode="before")
    def validate_and_convert_fields(cls, values):
        fields_to_validate = ["business_id", "owner_position_user_id", "recruiter_user_id"]
        for field in fields_to_validate:
            if field in values:
                if isinstance(values[field], ObjectId):
                    values[field] = str(values[field])
                elif not isinstance(values[field], str):
                    raise ValueError(f"Invalid {field} format. Must be a string or ObjectId.")

        # Validar y convertir user_id en responsible_users_ids
        if "responsible_users_ids" in values:
            for stakeholder in values["responsible_users_ids"]:
                if isinstance(stakeholder.user_id, ObjectId):
                    stakeholder.user_id = str(stakeholder.user_id)
                elif not isinstance(stakeholder.user_id, str):
                    raise ValueError("Invalid user_id format in responsible_users_ids. Must be a string or ObjectId.")

        return values


class GetPositionQueryParams(BaseModel):
    business_id: str
    user_id: str
    id: Optional[str] = None
    all: Optional[bool] = None

    @model_validator(mode="before")
    def check_id_or_all(cls, values):
        if not values.get("id") and not values.get("all"):
            raise ValueError("Either 'id' or 'all' query parameter is required")
        return values
    
    @model_validator(mode="before")
    def validate_and_convert_fields(cls, values):
        fields_to_validate = ["business_id", "user_id"]
        
        for field in fields_to_validate:
            if field in values:
                if isinstance(values[field], ObjectId):
                    values[field] = str(values[field])
                elif not isinstance(values[field], str):
                    raise ValueError(f"Invalid {field} format. Must be a string or ObjectId.")
        
        return values

    @classmethod
    def validate_params(cls, params):
        try:
            return cls(**params)
        except ValidationError as e:
            raise ValueError(f"Invalid query parameters: {e}")

class PositionEntity(BaseEntity[PositionDTO]):
    pass
