from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, ValidationError, model_validator

from src.domain.base_entity import BaseEntity


class STATUS(str, Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TYPE(str, Enum):
    AI_TEMPLATE = "AI_TEMPLATE"
    CUSTOM = "CUSTOM"
    OTHER_POSITION_AS_TEMPLATE = "OTHER_POSITION_AS_TEMPLATE"


class PHASE_TYPE(str, Enum):
    DESCRIPTION = "DESCRIPTION"
    SOFT_SKILLS = "SOFT_SKILLS"
    TECHNICAL_TEST = "TECHNICAL_TEST"
    FINAL_INTERVIEW = "FINAL_INTERVIEW"
    READY_TO_PUBLISH = "READY_TO_PUBLISH"


class Phase(BaseModel):
    name: str
    thread_id: str
    status: STATUS
    data: dict
    type: PHASE_TYPE


class PositionConfigurationDTO(BaseModel):
    user_id: str = Field(default="", alias="user_id")
    business_id: str = Field(default="", alias="business_id")
    status: STATUS = STATUS.DRAFT
    phases: Optional[List[Phase]] = Field(default=[])
    type: TYPE

    @model_validator(mode="before")
    def validate_and_convert_fields(cls, values):
        fields_to_validate = ["user_id", "business_id", "thread_id"]
        for field in fields_to_validate:
            if field in values:
                if isinstance(values[field], ObjectId):
                    values[field] = str(values[field])
                elif not isinstance(values[field], str):
                    raise ValueError(f"Invalid {field} format. Must be a string or ObjectId.")
        return values


class GetPositionConfigurationQueryParams(BaseModel):
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
        fields_to_validate = ["business_id"]

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

class ChatPositionConfigurationPayload(BaseModel):
    phase_type: PHASE_TYPE
    thread_id: str
    position_configuration_id: str
    business_id: str
    message: str

    @model_validator(mode="before")
    def validate_and_convert_fields(cls, values):
        fields_to_validate = ["business_id", "thread_id", "position_configuration_id"]

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


class PositionConfigurationEntity(BaseEntity[PositionConfigurationDTO]):
    pass
