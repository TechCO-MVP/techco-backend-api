import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import Response, content_types
from datetime import datetime, timedelta

from src.constants.index import TABLE_WEBSOCKET_CONNECTIONS

logger = Logger()
dynamodb = boto3.client("dynamodb")


@logger.inject_lambda_context
def handler(event, context):
    """handler new websocket conections."""
    connection_id = event["requestContext"]["connectionId"]
    
    try:
        user_id = event["requestContext"]["authorizer"]["user_id"]

        dynamodb.put_item(
            TableName=TABLE_WEBSOCKET_CONNECTIONS,
            Item={
                "user_id": {"S": user_id},
                "connection_id": {"S": connection_id},
                "expires_at": {"N": str(int((datetime.now() + timedelta(days=2)).timestamp()))},
            }
        )
        logger.info(f"WebSocket connected: {connection_id}")
        body = {
            "message": "connected",
            "body": {
                "connection_id": connection_id,
            },
        }
        return Response(status_code=200, body=body, content_type=content_types.APPLICATION_JSON)
    except Exception as e:
        body = {
            "message": str(e),
            "body": {
                "data": "Connection error",
            },
        }
        logger.error(f"Error handler WebSocket conection: {str(e)}")
        return Response(status_code=500, body=body, content_type=content_types.APPLICATION_JSON)