from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.profile import ProfileFilterProcessDTO, ProfileFilterProcessQueryDTO
from src.use_cases.profile.filter_profiles_ai_use_case import query_profiles_ai_use_case
from src.utils.errors import normalize_exception

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    try:
        logger.info("Querying openai data")
        logger.info(event)

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

        return query_profiles_ai_use_case(process_id, profile_filter_process)
    except Exception as e:
        normalized_exception = normalize_exception(e)
        normalized_exception.args[0]["event"] = event
        normalized_exception.args[0]["process_id"] = process_id
        logger.error(normalized_exception)
        raise normalized_exception
