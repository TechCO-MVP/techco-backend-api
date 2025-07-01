from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter


def get_message_history_by_therad_id_use_case(thread_id: str, params: dict) -> dict:
    """Get message history by thread id use case."""
    open_ai_adapter = OpenAIAdapter()
    limit = params.get("limit", "20")
    message_id = params.get("message_id", "")
    
    if len(message_id) < 10:
        message_id = None

    messages_history = open_ai_adapter.get_message_history(thread_id, limit, message_id)

    return messages_history
