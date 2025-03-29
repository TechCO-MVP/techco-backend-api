import boto3
import json
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

from src.domain.notification import NotificationDTO
from src.use_cases.notification.save_notification import post_notification_use_case
from src.constants.index import TABLE_WEBSOCKET_CONNECTIONS, REGION_NAME, ENV, API_ID

logger = Logger()
dynamodb = boto3.client("dynamodb")
url = f"https://{API_ID}.execute-api.{REGION_NAME}.amazonaws.com/{ENV}"
apigatewaymanagementapi = boto3.client("apigatewaymanagementapi", endpoint_url=url)


def send_message_by_websocket(notification: NotificationDTO):
    """Send a message to a WebSocket connection if it exists in DynamoDB."""
    logger.info(f"Sending message to user_id: {notification.user_id} via WebSocket")
    logger.info(f"Message content: {notification.message}")
    logger.info(f"save notificstion domain")
    post_notification_use_case(notification)
    
    try:
        logger.info(f"getting connection_id from DynamoDB for user_id: {notification.user_id}")
        response = dynamodb.query(
            TableName=TABLE_WEBSOCKET_CONNECTIONS,
            IndexName="user_id_index",
            KeyConditionExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": {"S": notification.user_id}},
        )
        logger.info(f"DynamoDB Query response: {response}")

        if not response["Items"]:
            logger.info(f"No active WebSocket connection found for user_id: {notification.user_id}")
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "No active WebSocket connection found"}),
            }

        connection_id = response["Items"][0]["connection_id"]["S"]

        logger.info(f"Found connection_id: {connection_id} for user_id: {notification.user_id}")
        logger.info("Sending message to connection_id")
        apigatewaymanagementapi.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({"message": notification.message}),
        )

        logger.info(f"Message sent to connection_id: {connection_id}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Message sent successfully"}),
        }

    except ClientError as e:
        logger.error(f"Error sending message: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Failed to send message", "error": str(e)}),
        }
