from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/pipefy/webhook")
def handler_pipefy_webhook():
    try:
        body = app.current_event.json_body
        logger.info(body)

        return Response(
            status_code=200,
            body={"message": "Webhook received successfully"},
            content_type=content_types.APPLICATION_JSON,
        )
    except Exception as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )


def lambda_hanlder(event: dict, context: LambdaContext) -> dict:
    """
    Lambda handler for pipefy webhook
    request: The request object, described like:
    {
        "body": {
        }
    }
    """
    return app.resolve(event, context)
