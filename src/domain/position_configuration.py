from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, model_validator

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
    thread_id: str = Field(default="", alias="thread_id")
    status: STATUS = STATUS.DRAFT
    phases: Optional[List[Phase]] = Field(default=[])
    type: TYPE
    
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
