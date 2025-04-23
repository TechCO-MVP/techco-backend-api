from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.use_cases.llm.message.get_message_history import get_message_history_by_therad_id_use_case


logger = Logger()
app = APIGatewayRestResolver()


@app.get("/llm/message_history")
def get_message_history():
    """Get message_history."""
    try:

        query_params = app.current_event.query_string_parameters
        thread_id = app.current_event.path_parameters.get("thread_id")
        response = get_message_history_by_therad_id_use_case(thread_id, query_params)

        message = "messages found successfully"

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
    Handler function for get user
    request: The request object, described like:
    {
        "queryStringParameters": {
            "limit": "number",
            "message_id": "string"
        }
        "pathParameters": {
            "thread_id": "string"
        }
    }
    """

    return app.resolve(event, context)
