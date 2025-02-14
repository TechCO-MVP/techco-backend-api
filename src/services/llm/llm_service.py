from abc import ABC, abstractmethod


class LLMService(ABC):
    """Abstract interface for the LLM service."""

    @abstractmethod
    def generate_response(self, prompt: str, file_path: str = None) -> str:
        """Generate a response to a prompt."""
        pass
