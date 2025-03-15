import json
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.constants.index import ENV

logger = Logger()
app = APIGatewayRestResolver()

eventbridge = boto3.client("events")


@app.post("/pipefy/webhook")
def handler_pipefy_webhook():
    try:
        body = app.current_event.json_body
        logger.info(body)

        action = body["data"]["action"]
        eventbridge.put_events(
            Entries=[
                {
                    "Source": "pipefy",
                    "DetailType": action,
                    "Detail": json.dumps(body),
                    "EventBusName": f"{ENV}-pipefy-event-bus",
                }
            ]
        )

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


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Lambda handler for pipefy webhook
    request: The request object, described like:
    {
        "body": {
        }
    }
    """
    return app.resolve(event, context)
