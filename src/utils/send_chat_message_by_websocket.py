import json

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

from src.constants.index import API_ID, ENV, REGION_NAME

logger = Logger()
dynamodb = boto3.client("dynamodb")
url = f"https://{API_ID}.execute-api.{REGION_NAME}.amazonaws.com/{ENV}"
apigatewaymanagementapi = boto3.client("apigatewaymanagementapi", endpoint_url=url)


def send_chat_message_by_websocket(connection_id: str, message: dict):
    """Send a chat message to a WebSocket connection if it exists in DynamoDB."""
    logger.info(f"Message content: {message}")

    try:
        logger.info("Sending message to connection_id")
        apigatewaymanagementapi.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({"action": message["type"], "payload": message.get("payload", {})}),
        )

        logger.info(f"Message sent to connection_id: {connection_id}")

        return True

    except ClientError as e:
        logger.error(f"Error sending message: {str(e)}")
        return False
