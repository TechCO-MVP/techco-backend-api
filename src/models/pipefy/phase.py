from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class IdentifyTaskEnum(str, Enum):
    anonymous = "anonymous"
    identified = "identified"


class FieldCondition(BaseModel):
    id: str
    name: Optional[str]
    phase_id: Optional[str]
    actions: Optional[List[str]]
    condition: Optional[str]
    isTrueFor: Optional[bool]
    url: Optional[str]


class PhaseField(BaseModel):
    id: str
    label: Optional[str]
    type: Optional[str]
    description: Optional[str]
    editable: Optional[bool]
    help: Optional[str]
    required: Optional[bool]
    sync_with_card: Optional[bool]
    minimal_view: Optional[bool]


class CardConnection(BaseModel):
    totalCount: int
    nodes: Optional[List[str]]


class Phase(BaseModel):
    id: str
    name: str
    uuid: str
    can_receive_card_directly_from_draft: Optional[bool]
    cards: Optional[CardConnection]
    cards_can_be_moved_to_phases: Optional[List[str]]
    cards_count: Optional[int]
    color: Optional[str]
    created_at: Optional[datetime]
    custom_sorting_preferences: Optional[str]
    description: Optional[str]
    done: bool
    expiredCardsCount: Optional[int]
    fieldConditions: Optional[List[FieldCondition]]
    fields: Optional[List[PhaseField]]
    identifyTask: Optional[IdentifyTaskEnum]
    index: Optional[float]
    isDraft: Optional[bool]
    lateCardsCount: Optional[int]
    lateness_time: Optional[int]
    next_phase_ids: Optional[List[str]]
    previous_phase_ids: Optional[List[str]]
    repo_id: Optional[int]
    sequentialId: Optional[str]
