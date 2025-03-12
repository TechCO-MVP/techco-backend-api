from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context
def lambda_habdler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to send reuqest to scraping profile filter process
    {
        "_id": "67aa9fe5e45a8924426e2ffa",
        "created_at": "2025-02-11T00:55:01.488274",
        "updated_at": "2025-02-11T00:55:01.488284",
        "deleted_at": null,
        "status": "in_progress",
        "execution_arn": "...",
        "user_id": "6791f6f8886eb975df789f6a",
        "position_id": "yyy",
        "business_id": "xxx",
        "process_filters": {
            "role": "Software Engineer",
            "seniority": "Senior",
            "country_code": "USA",
            "city": "San Francisco",
            "description": "...",
            "responsabilities": [...],
            "skills": [...],
            "business_id": "xxx",
            "position_id": "yyy",
            "snapshot_id": ""
        }
    }
    """
    logger.info("Starting filter profile by url")
    logger.info(event)
    logger.info(isinstance(event, dict))

    return event
