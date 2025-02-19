from enum import Enum
from typing import Any
from pydantic import BaseModel


class OPEN_AI_ROLE(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class OpenAIMessage(BaseModel):
    role: OPEN_AI_ROLE
    content: str
    require_placeholders: bool


class OpenAITool(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]
