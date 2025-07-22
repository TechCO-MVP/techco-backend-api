from enum import Enum
from typing import Dict, Optional, List

from pydantic import BaseModel, model_validator

from src.domain.assistant import Assistant
from src.domain.base_entity import BaseEntity
from src.domain.position_configuration import FLOW_TYPE
from src.domain.defaults.business import DEFAULT_EVALUATION_WEIGHTS


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


class CRITERION_TYPE(str, Enum):
    TALENT_DNA = "TALENT_DNA"
    CHALLENGES_AND_BEHAVIORS_RESULT = "CHALLENGES_AND_BEHAVIORS_RESULT"
    FIRST_INTERVIEW = "FIRST_INTERVIEW"
    BUSINESS_CASE_RESULT = "BUSINESS_CASE_RESULT"
    FINAL_INTERVIEW = "FINAL_INTERVIEW"


class EvaluationCriterion(BaseModel):
    name: str
    criterion_type: CRITERION_TYPE
    weight: float


class BusinessConfigurationDTO(BaseModel):
    evaluation_weights: List[EvaluationCriterion] = [
        EvaluationCriterion(**weight) for weight in DEFAULT_EVALUATION_WEIGHTS
    ]

    @model_validator(mode="before")
    def validate_and_convert_fields(cls, values):
        if "evaluation_weights" in values:
            if isinstance(values["evaluation_weights"], list):
                values["evaluation_weights"] = [
                    EvaluationCriterion(**weight) for weight in values["evaluation_weights"]
                ]
                total_weight = sum(ec.weight for ec in values["evaluation_weights"])
            if abs(total_weight - 100) > 1e-6:
                raise ValueError("Sum of all weights must be 100%")
            else:
                raise ValueError("evaluation_weights must be a list of EvaluationCriterion objects")
        return values


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
