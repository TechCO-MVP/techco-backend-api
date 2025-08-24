from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(service="process_cv_profile_filter")


@logger.inject_lambda_context
def handler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to send request to process CV profile filter
    {
        "_id": "67aa9fe5e45a8924426e2ffa",
        "created_at": "2025-02-11T00:55:01.488274",
        "updated_at": "2025-02-11T00:55:01.488284",
        "deleted_at": null,
        "status": "in_progress",
        "execution_arn": null,
        "user_id": "6791f6f8886eb975df789f6a",
        "position_id": "yyy",
        "business_id": "xxx",
        "process_filters": {
            "role": "Software Engineer",
            "seniority": "Senior",
            "country_code": "USA",
            "city": "San Francisco",
            "description": (
                "Experienced software engineer with expertise in Python and cloud technologies."
            ),
            "responsabilities": [
                "Design and develop scalable and maintainable software solutions.",
            ],
            "skills": [
                {
                    "name": "Python",
                    "required": true
                },
            ],
            "business_id": "xxx",
            "position_id": "yyy",
        }
    }
    """
    logger.info("Processing CV profile filter...")
    logger.info(event)
    logger.info(context)

    try:
        return {**event}
    except Exception as e:
        logger.exception(e)
        return {"status": "Error", "errorInfo": e.args[0]}
