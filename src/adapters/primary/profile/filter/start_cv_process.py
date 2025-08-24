import base64

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.use_cases.profile.save_cv_profile_filter import (
    save_cv_profile_filter_use_case,
    start_filter_profile_csv_use_case,
)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/profile/filter/start/cv")
def start_cv_process():
    """Start CV profile filter process."""
    try:
        logger.info(f"Raw event: {app.current_event.raw_event}")
        logger.info(f"Headers: {app.current_event.headers}")

        body = app.current_event.body
        is_base64_encoded = app.current_event.raw_event.get("isBase64Encoded", False)

        if is_base64_encoded:
            body = base64.b64decode(body)
        elif isinstance(body, str):
            body = body.encode("utf-8")

        content_type = app.current_event.headers.get("Content-Type", "")
        headers = app.current_event.headers

        file_key, position_id, business_id = save_cv_profile_filter_use_case(
            body, content_type, headers
        )

        result = start_filter_profile_csv_use_case(position_id, business_id, file_key)

        return Response(
            status_code=200,
            body={
                "message": "Process started successfully",
                "body": {
                    "data": {
                        "file_key": file_key,
                        "position_id": position_id,
                        "business_id": business_id,
                        "filter_profile": result.get("filter_profile"),
                    }
                },
            },
            content_type=content_types.APPLICATION_JSON,
        )

    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=422, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "Internal server error"},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for starting CV profile filter process
    request: The request object, described like:
    {
        "body": {
            "file": "string", // actual file content or base64 encoded string
            "position_id": "string",
            "business_id": "string"
        }
    }
    response: The response object, described like:
    {
        "message": "Process started successfully",
        "body": {
            "data": {
                "message": "string",
                "process_id": "string"
            }
        }
    }
    """
    if event.get("source") == "serverless-plugin-warmup":
        logger.info("Warmup event detected. Exiting.")
        return {"status": "Warmup event"}

    return app.resolve(event, context)
