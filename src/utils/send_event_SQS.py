import boto3
import json
import os


def send_event_SQS(message_body:dict, queue_name:str, message_group_id:str="default") -> bool:
    sqs_client = boto3.client('sqs', region_name=os.getenv('REGION_NAME'))

    try:
        response = sqs_client.send_message(
            QueueUrl=queue_name,
            MessageBody=json.dumps(message_body),
            MessageGroupId=message_group_id
        )
        print(response)

        return True
    
    except Exception as e:
        print(e)
        return False
