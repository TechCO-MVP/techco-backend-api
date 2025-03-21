import boto3
import json
from aws_lambda_powertools import Logger

from src.constants.index import TABLE_WEBSOCKET_CONNECTIONS

logger = Logger()
dynamodb = boto3.client("dynamodb")


@logger.inject_lambda_context
def handler(event, context):
    """Maneja desconexiones WebSocket."""
    logger.info(f"Event: {event}")
    connection_id = event["requestContext"]["connectionId"]
    
    try:
        dynamodb.delete_item(
            TableName=TABLE_WEBSOCKET_CONNECTIONS,
            Key={
                "connection_id": {"S": connection_id}
            }
        )
        logger.info(f"WebSocket disconected: {connection_id}")
        body = json.dumps(
            {
                "message": "Disconnected",
                "body": {
                    "connection_id": connection_id,
                },
            }
        )
        return {"statusCode": 200, "body": body}
    except Exception as e:
        logger.error(f"Error handler disconnetion: {str(e)}")
        body = json.dumps(
            {
                "message": str(e),
                "body": {
                    "data": "Error while disconnecting",
                },
            }
        )
        return {"statusCode": 500, "body": body}