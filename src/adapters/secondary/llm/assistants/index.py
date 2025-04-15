from typing import Any

from src.domain.assistant import ASSISTANT_TYPE
from src.adapters.secondary.llm.assistants.position_assistant import (
    config as position_assistant_config,
)

config_map = {
    ASSISTANT_TYPE.POSITION_ASSISTANT: position_assistant_config,
    ASSISTANT_TYPE.TECHNICAL_ASSESSMENT_ASSISTANT: None,
}


def get_config_by_type(assistant_type: str) -> dict[str, Any]:
    if assistant_type not in config_map:
        raise ValueError(f"Invalid assistant type: {assistant_type}")

    if config_map[assistant_type] is None:
        raise ValueError(f"Assistant type {assistant_type} is not configured.")

    return config_map[assistant_type]
