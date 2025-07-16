import traceback

from aws_lambda_powertools import Logger

from src.use_cases.profile.pipefy.create_pipe_configuration_open_position import (
    create_pipe_configuration_open_position,
)

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event: dict, _):
    try:

        logger.info("Creating pipe and webhooks for open position")
        logger.info(event)

        process_id: str = event.get("_id", None)
        if not process_id:
            raise Exception("The id is required")

        position_id: str = event.get("position_id", None)
        if not position_id:
            raise Exception("The position_id is required")

        business_id: str = event.get("business_id", None)
        if not business_id:
            raise Exception("The business_id is required")

        event = create_pipe_configuration_open_position(process_id, position_id, business_id)

        return event
    except Exception as e:
        logger.error(f"Error creating pipe configuration for open position: {e}")
        return {
            "Type": "Fail",
            "Status": "ERROR",
            "ErrorInfo": "Error creating pipe configuration for open position",
            "ErrorDetails": f"{e} - {traceback.format_exc()}",
        }
