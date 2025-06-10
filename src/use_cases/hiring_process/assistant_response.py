import json
from aws_lambda_powertools import Logger

from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.business_repository import BusinessRepository
from src.domain.assistant import ASSISTANT_TYPE

from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter

logger = Logger()


def assistant_response_use_case(
    hiring_process_id: str, run_id: str, thread_id: str, assistant_type: ASSISTANT_TYPE
) -> dict:
    """
    Use case to handle the assistant response in the hiring process.

    Args:
        hiring_process_id (str): The ID of the hiring process.
        run_id (str): The ID of the run for the assistant response.
        thread_id (str): The ID of the thread for the assistant response.
        assistant_type (ASSISTANT_TYPE): The type of assistant to use.

    Returns:
        dict: The response from the assistant.
    """
    logger.info(f"Assistant response use case started for hiring process ID: {hiring_process_id}")

    hiring_repository = HiringProcessRepository()
    hiring_process = hiring_repository.getById(hiring_process_id)

    if not hiring_process:
        raise ValueError("Hiring process not found")

    bussiness_repository = BusinessRepository()
    business = bussiness_repository.getById(hiring_process.props.business_id)
    if not business:
        raise ValueError("Business not found")

    assistants = business.props.assistants
    if assistant_type not in assistants:
        raise ValueError("Assistant type not found in business")

    if assistants.get(assistant_type) is None:
        raise ValueError("Assistant not found")

    open_ai_adapter = OpenAIAdapter({"business_id": business.id})
    open_ai_adapter.assistant_id = assistants[assistant_type].assistant_id

    logger.info(f"Checking status for Run ID: {run_id}")

    thread_run = open_ai_adapter.client.beta.threads.runs.retrieve(
        run_id=run_id, thread_id=thread_id
    )
    response = json.loads(open_ai_adapter.run_and_process_thread(thread_run))

    return response
