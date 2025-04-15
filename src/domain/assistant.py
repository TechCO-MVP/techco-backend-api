from enum import Enum
from pydantic import BaseModel


class ASSISTANT_TYPE(str, Enum):
    POSITION_ASSISTANT = "position_assistant"
    TECHNICAL_ASSESSMENT_ASSISTANT = "technical_assessment_assistant"


class Assistant(BaseModel):
    assistant_type: ASSISTANT_TYPE
    assistant_id: str
