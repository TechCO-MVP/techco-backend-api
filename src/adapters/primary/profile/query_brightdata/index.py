from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.profile import ProfileFilterProcessQueryDTO
from src.use_cases.profile.send_profile_query import send_profile_query_use_case

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to list businesses by user
    """
    logger.info("Querying brightdata")
    logger.info(event)
    logger.info(context)

    profile_process_dto = ProfileFilterProcessQueryDTO(**event)
    snapshot_id = send_profile_query_use_case(profile_process_dto)
    event["snapshot_id"] = snapshot_id

    return event
