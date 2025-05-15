from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.use_cases.position.get_position_by_token import get_position_by_token_use_case
from src.use_cases.position.get_position_by_id_for_vacancy_public_page import get_position_by_id_for_vacancy_public_page

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/position/token")
def get_position_by_token():
    """Get position by token or by position_id for vacancy page"""
    try:

        query_params = app.current_event.query_string_parameters
        response = None

        if query_params.get("position_id"):
            response = get_position_by_id_for_vacancy_public_page(query_params)
        elif query_params.get("token"):
            response = get_position_by_token_use_case(query_params)
        
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
            "token": "string",
        }
    }
    """

    return app.resolve(event, context)
