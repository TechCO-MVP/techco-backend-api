from typing import List
from src.models.openai.index import OpenAIMessage


def format_placeholders(message: str, placeholders: dict) -> str:
    """
    Format a message with placeholders.
    """
    return message.format(**placeholders)


def format_prompts_placeholders(prompts: List[OpenAIMessage], placeholders: List[dict]) -> list:
    """
    Format a list of prompts with placeholders.
    """
    formatted_prompts = []
    for prompt in prompts:
        if prompt.require_placeholders:
            content = format_placeholders(prompt.content, placeholders.pop(0))
        else:
            content = prompt.content

        formatted_prompts.append({"role": prompt.role, "content": content})

    return formatted_prompts
