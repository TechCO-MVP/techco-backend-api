from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from src.domain.base_entity import BaseEntity
from src.domain.profile import ProfileBrightDataDTO
from src.domain.assistant import ASSISTANT_TYPE
from src.domain.assistant import Assistant


class HIRING_PROCESS_STATUS(str, Enum):
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class HiringProcessPhaseField(BaseModel):
    field_id: str
    label: str
    value: Any


class HiringProcessPhase(BaseModel):
    phase_id: int
    fields: dict[str, HiringProcessPhaseField] = {}


class PhaseMove(BaseModel):
    phase_id: int
    name: str


class HiringProcessPhaseHistory(BaseModel):
    from_phase: PhaseMove
    to_phase: PhaseMove
    date: datetime = Field(default_factory=datetime.now)


class Assistant(BaseModel):
    assistant_type: ASSISTANT_TYPE
    thread_id: str
    data: dict[str, Any] = {}

class HiringProcessDTO(BaseModel):
    position_id: str = Field(..., alias="position_id")
    business_id: str = Field(..., alias="business_id")
    card_id: str = Field(...)
    phase_id: str = Field(...)
    status: HIRING_PROCESS_STATUS = HIRING_PROCESS_STATUS.STARTED
    profile: ProfileBrightDataDTO = Field(...)
    phases: dict[str, HiringProcessPhase] = {}
    phase_history: List[HiringProcessPhaseHistory] = []
    assesments: Dict[str, Phase] = {}

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


class UpdateHiringProcessDTO(BaseModel):
    id: str = Field(...)
    phase_id: Optional[str]
    status: Optional[HIRING_PROCESS_STATUS]
    profile: Optional[ProfileBrightDataDTO]
    phases: Optional[dict[str, HiringProcessPhase]]
    phase_history: Optional[List[HiringProcessPhaseHistory]]
    assistants: Optional[dict[str, Assistant]]


class HiringProcessEntity(BaseEntity[HiringProcessDTO]):
    pass
