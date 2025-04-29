from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.use_cases.position_configuration.complete_phase import (
    complete_phase_position_configuration_use_case,
)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/position_configuration/complete/phase")
def complete_phase():
    """Complete phase."""
    try:
        body = app.current_event.json_body
        logger.info(f"Received body: {body}")

        # Validate the body
        if not body.get("position_configuration_id"):
            raise ValueError("position_configuration_id is required")

        if not body.get("data") or not isinstance(body["data"], dict):
            raise ValueError("data is required")

        authorizer = app.current_event.request_context.authorizer["claims"]
        user_email = authorizer["email"]

        response = complete_phase_position_configuration_use_case(
            body["position_configuration_id"], body["data"], user_email
        )
        logger.info(f"Response from use case: {response}")

        return Response(
            status_code=200,
            body={
                "message": "Phase completed successfully",
                "body": {
                    "data": response.to_dto(flat=True),
                },
            },
            content_type=content_types.APPLICATION_JSON,
        )

    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=422, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except Exception as e:
        logger.error(f"Error in complete_phase handler: {str(e)}")
        return Response(
            status_code=500,
            body={"message": "Internal server error"},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event, context: LambdaContext) -> dict:
    """
    Handler function for phase completion.
    request: {
        "body": {
            "position_configuration_id": "12345",
            "data": {...}
        }
    }
    """
    return app.resolve(event, context)
