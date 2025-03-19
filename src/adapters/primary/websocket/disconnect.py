import boto3
import os
from aws_lambda_powertools import Logger

logger = Logger()
dynamodb = boto3.client('dynamodb')
table_name = f"{os.environ['SERVICE_NAME']}-{os.environ['STAGE']}-websocket-connections"

@logger.inject_lambda_context
def handler(event, context):
    """Maneja desconexiones WebSocket."""
    connection_id = event['requestContext']['connectionId']
    
    try:
        # Elimina el ID de conexión de DynamoDB
        dynamodb.delete_item(
            TableName=table_name,
            Key={
                'connectionId': {'S': connection_id}
            }
        )
        logger.info(f"WebSocket desconectado: {connection_id}")
        return {'statusCode': 200, 'body': 'Desconectado'}
    except Exception as e:
        logger.error(f"Error al manejar desconexión WebSocket: {str(e)}")
        return {'statusCode': 500, 'body': 'Error al desconectar'}