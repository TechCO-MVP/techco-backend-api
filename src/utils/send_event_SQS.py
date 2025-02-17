import boto3
import os

def send_event_SQS(message_body, queue_name):
    sqs_client = boto3.client('sqs', region_name=os.getenv('REGION_NAME'))

    try:
        response = sqs_client.get_queue_url(QueueName=queue_name)
        print('response sqs', response)
        queue_url = response['QueueUrl']

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(response)

        return response
    
    except Exception as e:
        print(e)
        return False
