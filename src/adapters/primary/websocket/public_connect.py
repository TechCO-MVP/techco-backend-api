import boto3
import json
from aws_lambda_powertools import Logger
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from src.constants.index import TABLE_WEBSOCKET_CONNECTIONS_PUBLIC, API_ID, REGION_NAME, ENV

logger = Logger()
dynamodb = boto3.client("dynamodb")
url = f"https://{API_ID}.execute-api.{REGION_NAME}.amazonaws.com/{ENV}"
apigatewaymanagementapi = boto3.client("apigatewaymanagementapi", endpoint_url=url)


@logger.inject_lambda_context
def handler(event, context):
    """handler new websocket conections."""
    connection_id = event["requestContext"]["connectionId"]
    
    try:
        query_params = event.get("queryStringParameters", {}) or {}
        hiring_process_id = query_params.get("hiring_process_id")

        verify_connection(hiring_process_id)

        dynamodb.put_item(
            TableName=TABLE_WEBSOCKET_CONNECTIONS_PUBLIC,
            Item={
                "hiring_process_id": {"S": hiring_process_id},
                "connection_id": {"S": connection_id},
                "expires_at": {"N": str(int((datetime.now() + timedelta(days=2)).timestamp()))},
            }
        )
        logger.info(f"WebSocket connected: {connection_id}")
        body = json.dumps(
            {
                "message": "connected",
                "body": {
                    "connection_id": connection_id,
                },
            }
        )
        logger.info(f"response body: {body}")
        return {"statusCode": 200, "body": body}
    except Exception as e:
        body = json.dumps(
            {
                "message": str(e),
                "body": {
                    "data": "Connection error",
                },
            }
        )
        logger.error(f"Error handler WebSocket conection: {str(e)}")
        return {"statusCode": 500, "body": body}
    
def verify_connection(hiring_process_id: str):
    """Verify if exist an active connection."""
    response = dynamodb.query(
        TableName=TABLE_WEBSOCKET_CONNECTIONS_PUBLIC,
        IndexName="hiring_process_id_index",
        KeyConditionExpression="hiring_process_id = :hiring_process_id",
        ExpressionAttributeValues={":hiring_process_id": {"S": str(hiring_process_id)}},
    )

    if response.get("Items"):
        existing_connection_id = response["Items"][0]["connection_id"]["S"]
        logger.info(
            f"Connection already exists for {hiring_process_id=}, deleting connection {existing_connection_id=}"
        )

        close_connection(existing_connection_id)

def close_connection(connection_id: str):
    """Close connection in websocket api."""
    try:
        apigatewaymanagementapi.delete_connection(ConnectionId=connection_id)
    except ClientError as e:
        if e.response["Error"]["Code"] == "GoneException":
            logger.info(f"Existing connection {connection_id=} already closed")
        else:
            logger.error(f"Error closing connection {connection_id=}: {e}")
            raise e
