from aws_lambda_powertools import Logger
from src.use_cases.profile.pipefy.create_cards_for_profiles_use_case import (
    create_cards_for_profiles_use_case,
)

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event: dict, _):
    """
    Lambda handler for creating cards for profiles
    """
    try:
        logger.info("Creating cards for profiles")
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

        result = create_cards_for_profiles_use_case(process_id, position_id, business_id)

        logger.info("Cards created successfully")
        return result

    except Exception as e:
        logger.error(f"Error creating cards for profiles: {e}")
        raise e
