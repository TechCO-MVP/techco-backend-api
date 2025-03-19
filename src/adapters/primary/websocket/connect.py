import boto3
import os
from aws_lambda_powertools import Logger

logger = Logger()
dynamodb = boto3.client('dynamodb')
table_name = f"{os.getenv['SERVICE_NAME']}-{os.getenv['STAGE']}-websocket-connections"

@logger.inject_lambda_context
def handler(event, context):
    """Maneja conexiones WebSocket nuevas."""
    connection_id = event['requestContext']['connectionId']
    
    try:
        user_id = event["requestContext"]["authorizer"]["user_id"]
        # Almacena el ID de conexión en DynamoDB
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'user_id': {'S': user_id},
                'connection_id': {'S': connection_id}
            }
        )
        logger.info(f"WebSocket conectado: {connection_id}")
        return {'statusCode': 200, 'body': 'Conectado'}
    except Exception as e:
        logger.error(f"Error al manejar conexión WebSocket: {str(e)}")
        return {'statusCode': 500, 'body': 'Error al conectar'}