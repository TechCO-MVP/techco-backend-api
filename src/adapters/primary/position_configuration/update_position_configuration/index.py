from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.position_configuration import PositionConfigurationDTO
from src.use_cases.position_configuration.put_position_configuration import put_position_configuration_use_case


logger = Logger()
app = APIGatewayRestResolver()


@app.put("/position_configuration/update")
def put_position_configuration():
    """Put position configuration."""
    try:
        
        body = app.current_event.json_body
        
        PositionConfigurationDTO(**body)
        
        response = put_position_configuration_use_case(body)

        return Response(
            status_code=200,
            body={
                "message": "Position configuration updated successfully",
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
            "thread_id": string,
            "status": string,
            "phases": [
                {
                    "name": string,
                    "thread_id": string,
                    "status": string,
                    "data": dict
                    "type": string
                }
            ],
            "type": string,
        }
    }
    """

    return app.resolve(event, context)
