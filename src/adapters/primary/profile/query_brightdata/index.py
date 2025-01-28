from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to list businesses by user
    """
    logger.info("Querying brightdata")
    logger.info(event)
    logger.info(context)

    return {"message": "Querying brightdata"}
