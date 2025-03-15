from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.position import GetPositionQueryParams
from src.use_cases.position.get_position import get_position_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/position/list")
def get_position():
    """Get position."""
    try:

        authorizer = app.current_event.request_context.authorizer["claims"]
        user_email = authorizer["email"]
        
        query_params = app.current_event.query_string_parameters
        GetPositionQueryParams.validate_params(query_params)

        response = get_position_use_case(query_params, user_email)

        message = "Position found successfully" if response else "Position not found"

        return Response(
            status_code=200,
            body={
                "message": message,
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
    Handler function for get position
    request: The request object, described like:
    {
        "queryStringParameters": {
            "id": "string",
            "all": "boolean"
        }
    }
    """

    return app.resolve(event, context)
