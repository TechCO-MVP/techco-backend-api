from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.use_cases.profile.filter_profiles_ai_use_case import query_profiles_ai_use_case

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info("Querying brightdata")
    logger.info(event)

    process_id: str = event.get("_id", None)
    if not process_id:
        return {"message": "The id is required"}

    query_profiles_ai_use_case(process_id, event)

    return event
