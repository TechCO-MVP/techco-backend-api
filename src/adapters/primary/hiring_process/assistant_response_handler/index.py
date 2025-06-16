from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.use_cases.hiring_process.assistant_response_handler import (
    assistant_response_handler_use_case,
)

logger = Logger()
app = APIGatewayRestResolver()


def hiring_process_assistant_response_handler(event: dict, context: LambdaContext) -> dict:
    try:
        logger.info(f"Received event: {event}")
        hiring_process_id = event.get("hiring_process_id")
        run_id = event.get("run_id")
        thread_id = event.get("thread_id")
        assistant_name = event.get("assistant_name")

        if not hiring_process_id:
            raise ValueError("hiring_process_id is required")
        if not run_id:
            raise ValueError("run_id is required")
        if not thread_id:
            raise ValueError("thread_id is required")
        if not assistant_name:
            raise ValueError("assistant_name is required")

        response = assistant_response_handler_use_case(
            hiring_process_id, run_id, thread_id, assistant_name
        )

        return {
            **event,
            **response,
        }
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise e


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
        Handler function for send file to assistant
    request: The request object, described like:
    {
        "body": {
            "hiring_process_id": "string",
            "run_id": "string",
            "thread_id": "string",
            "assistan_type": "string"
        }
    }
    """
    return hiring_process_assistant_response_handler(event, context)
