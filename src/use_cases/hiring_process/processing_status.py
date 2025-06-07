import boto3
import os
from datetime import datetime, timedelta

from src.constants.index import ENV


def save_processing_status(process_id: str, thread_id: str, status: str):
    """Save the processing status to DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(f"{ENV}-file-processing-status")
    
    expires_at = int((datetime.now() + timedelta(hours=24)).timestamp())
    
    table.put_item(
        Item={
            'process_id': process_id,
            'thread_id': thread_id,
            'status': status,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at
        }
    )

def get_processing_status(process_id: str) -> dict:
    """Get the processing status from DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(f"{ENV}-file-processing-status")
    
    response = table.get_item(
        Key={
            'process_id': process_id
        }
    )
    
    return response.get('Item')