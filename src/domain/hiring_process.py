from datetime import datetime
from enum import Enum
from typing import Any, List

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from src.domain.base_entity import BaseEntity
from src.domain.profile import ProfileBrightDataDTO


class HIRING_PROCESS_STATUS(str, Enum):
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class HiringProcessPhaseField(BaseModel):
    field_id: str
    label: str
    value: Any


class HiringProcessPhase(BaseModel):
    phase_id: str
    name: str
    fields: List[HiringProcessPhaseField] = []


class PhaseMove(BaseModel):
    phase_id: str
    name: str


class HiringProcessPhaseHistory(BaseModel):
    from_phase: PhaseMove
    to_phase: PhaseMove
    date: datetime = Field(default_factory=datetime.now)


class HiringProcessDTO(BaseModel):
    position_id: str = Field(..., alias="position_id")
    business_id: str = Field(..., alias="business_id")
    card_id: str = Field(...)
    phase_id: str = Field(...)
    status: HIRING_PROCESS_STATUS = HIRING_PROCESS_STATUS.STARTED
    profile: ProfileBrightDataDTO = Field(...)
    phases: List[HiringProcessPhase] = []
    phase_history: List[HiringProcessPhaseHistory] = []

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


class HiringProcessEntity(BaseEntity[HiringProcessDTO]):
    pass
