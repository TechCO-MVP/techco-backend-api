from enum import Enum
from typing import Any
from pydantic import BaseModel


class OPEN_AI_ROLE(str, Enum):
    USER = "user"
    SYSTEM = "system"


class OpenAIMessage(BaseModel):
    role: OPEN_AI_ROLE
    content: str


class OpenAITool(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]
