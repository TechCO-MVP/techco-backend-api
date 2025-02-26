import traceback
from aws_lambda_powertools import Logger
from src.use_cases.profile.pipefy.create_pipe_configuration_open_position import (
    create_pipe_configuration_open_position,
)

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event: dict, _):
    try:

        logger.info("Creating pipe configuration for open position")
        logger.info(event)

        process_id: str = event.get("_id", None)
        if not process_id:
            raise Exception("The id is required")

        create_pipe_configuration_open_position(process_id)

        return event
    except Exception as e:
        logger.error(f"Error creating pipe configuration for open position: {e}")
        return {
            "status": "ERROR",
            "error_message": "Error creating pipe configuration for open position",
            "error_details": f"{e} - {traceback.format_exc()}",
        }
