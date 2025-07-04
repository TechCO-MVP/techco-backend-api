from enum import Enum
from typing import Dict, List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, ValidationError, model_validator

from src.domain.base_entity import BaseEntity
from src.domain.assistant import Assistant
from src.domain.business import PositionFlow
from src.domain.position_configuration import FLOW_TYPE, PHASE_TYPE


class POSITION_STATUS(str, Enum):
    CANCELED = "CANCELED"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    INACTIVE = "INACTIVE"
    DRAFT = "DRAFT"


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
    currency: Optional[str] = None
    salary: Optional[str] = None
    salary_range: Optional[Range] = None


class PositionStakeholders(BaseModel):
    user_id: str
    can_edit: bool


class COUNTRY_CODE(str, Enum):
    CO = "CO"
    PE = "PE"
    MX = "MX"


class Assessments(BaseModel):
    data: dict
    type: PHASE_TYPE


class PositionDTO(BaseModel):
    position_configuration_id: str = Field(default="", alias="position_configuration_id")
    business_id: str = Field(default="", alias="business_id")
    owner_position_user_id: str
    recruiter_user_id: Optional[str] = ""
    responsible_users: List[PositionStakeholders] = Field(default_factory=list)
    flow_type: FLOW_TYPE
    role: str
    seniority: str
    country_code: COUNTRY_CODE
    city: str
    description: str
    responsabilities: List[str] = Field(..., min_length=1)
    education: Optional[List[str]] = Field(default_factory=list)
    skills: List[Skill] = Field(..., min_length=1)
    languages: Optional[List[Languages]] = Field(default_factory=list)
    hiring_priority: LEVEL
    work_mode: WORK_MODE
    status: POSITION_STATUS = POSITION_STATUS.DRAFT
    benefits: Optional[List[str]] = Field(default_factory=list)
    salary: Optional[Salary] = Field(default=None)
    pipe_id: Optional[str] = None
    assistants: Dict[str, Assistant] = {}
    position_flow: Optional[PositionFlow] = None
    assessments: Optional[List[Assessments]] = Field(default_factory=list)

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
                    raise ValueError(
                        "Invalid user_id format in responsible_users_ids. "
                        "Must be a string or ObjectId."
                    )

        return values


class GetPositionQueryParams(BaseModel):
    business_id: str
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


class UpdatePositionStatusDTO(BaseModel):
    position_id: str
    user_id: str
    position_status: POSITION_STATUS = POSITION_STATUS.ACTIVE

    @classmethod
    def validate_params(cls, params):
        try:
            return cls(**params)
        except ValidationError as e:
            raise ValueError(f"Invalid parameters: {e}")


class PositionEntity(BaseEntity[PositionDTO]):
    pass
