from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel

from src.domain.assistant import Assistant
from src.domain.base_entity import BaseEntity
from src.domain.position_configuration import FLOW_TYPE


class BUSINESS_SIZE(str, Enum):
    SMALL = "A"
    MEDIUM = "B"
    LARGE = "C"
    ENTERPRISE = "D"


class PHASE_CLASSIFICATION(str, Enum):
    INFORMATIVE = "INFORMATIVE"
    CALL_TO_ACTION = "CALL_TO_ACTION"


class PhaseSection(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    button_text: Optional[str] = None


class PhaseMetadata(BaseModel):
    sections: Optional[list[PhaseSection]] = []


class Phase(BaseModel):
    name: str
    phase_classification: PHASE_CLASSIFICATION
    candidate_data: Optional[PhaseMetadata] = None
    interviewer_data: Optional[PhaseMetadata] = None


class Group(BaseModel):
    name: str
    phases: list[Phase] = []


class PositionFlow(BaseModel):
    flow_type: FLOW_TYPE
    pipe_id: int
    groups: list[Group] = []


class BusinessDTO(BaseModel):
    name: str
    country_code: str
    company_size: BUSINESS_SIZE
    is_admin: bool = False
    logo: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    linkedin_url: Optional[str] = None
    segment: Optional[str] = None
    industry: Optional[str] = None
    parent_business_id: Optional[str] = None
    assistants: Dict[str, Assistant] = {}
    position_flows: Optional[Dict[FLOW_TYPE, PositionFlow]] = {}


class BusinessEntity(BaseEntity[BusinessDTO]):
    def get_parent_business_id(self) -> str:
        if self.props.is_admin:
            return self.id

        return self.props.parent_business_id
