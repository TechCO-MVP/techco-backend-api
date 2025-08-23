from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.position import UpdatePositionStatusDTO
from src.use_cases.position.put_position_status import put_position_status_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.put("/position/status")
def put_position_status():
    """Put position status."""
    try:

        body = app.current_event.json_body
        update_status_dto = UpdatePositionStatusDTO(**body)

        response = put_position_status_use_case(update_status_dto)

        return Response(
            status_code=200,
            body={
                "message": "Position updated successfully",
                "body": {
                    "data": response,
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
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for put position status
    request: The request object, described like:
    {
        "body": {
            "position_id": "string",
            "position_status": "string",
            "user_id": "string"
        }
    }
    """

    return app.resolve(event, context)
