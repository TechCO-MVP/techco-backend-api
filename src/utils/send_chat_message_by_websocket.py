import boto3
import json
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

from src.constants.index import REGION_NAME, ENV, API_ID

logger = Logger()
dynamodb = boto3.client("dynamodb")
url = f"https://{API_ID}.execute-api.{REGION_NAME}.amazonaws.com/{ENV}"
apigatewaymanagementapi = boto3.client("apigatewaymanagementapi", endpoint_url=url)


def send_chat_message_by_websocket(user_id: str, connection_id: str, message: dict):
    """Send a chat message to a WebSocket connection if it exists in DynamoDB."""
    logger.info(f"Rresponse message to user_id: {user_id} via WebSocket")
    logger.info(f"Message content: {message}")
    
    try:
        logger.info("Sending message to connection_id")
        apigatewaymanagementapi.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({"action": message["type"], "payload": {"message": message["message"]}}),
        )

        logger.info(f"Message sent to connection_id: {connection_id}")
        
        return True

    except ClientError as e:
        logger.error(f"Error sending message: {str(e)}")
        return False
