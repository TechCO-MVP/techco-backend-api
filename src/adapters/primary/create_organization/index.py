# lambda implementation
import json


def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Go Serverless v1.0! Your function executed successfully!",
                "input": event,
            }
        ),
    }
