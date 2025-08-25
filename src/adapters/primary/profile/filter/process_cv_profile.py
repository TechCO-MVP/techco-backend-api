from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.profile import ProfileFilterProcessDTO, ProfileFilterProcessQueryDTO
from src.use_cases.profile.process_cv_profile_use_case import process_cv_profile_use_case

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
        process_id: str = event.get("_id", None)
        if not process_id:
            return {
                "status": "ERROR",
                "error_message": "The id is required",
                "error_details": "The id is required",
            }

        profile_filter_process = ProfileFilterProcessDTO(
            status=event.get("status"),
            execution_arn=event.get("execution_arn"),
            user_id=event.get("user_id"),
            position_id=event.get("position_id"),
            company_id=event.get("company_id"),
            process_filters=ProfileFilterProcessQueryDTO(**event.get("process_filters", {})),
        )

        return process_cv_profile_use_case(process_id, profile_filter_process)
    except Exception as e:
        logger.exception(e)
        return {"status": "Error", "errorInfo": e.args[0]}
