""" this module is responsible for starting the authentication passwordless process """

import json
import boto3
from botocore.exceptions import ClientError
from src.constants.index import REGION_NAME, CLIENT_ID

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)


def lambda_handler(event, context):
    """
    send request to cognito to start the authentication process
    """
    body = json.loads(event["body"])
    user_email = body["email"]
    client_id = CLIENT_ID
    status_code = 400
    success = False
    body = {}

    try:
        response = cognito_client.initiate_auth(
            AuthFlow="CUSTOM_AUTH", AuthParameters={"USERNAME": user_email}, ClientId=client_id
        )
        session = response["Session"]
        status_code = 200
        body = {"message": "OTP sent successfully.", "session": session}
        success = True

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        body = {"error": f"Failed to start authentication: {error_message}"}

    except Exception as e:
        status_code = 500
        body = {"error": f"Unexpected error: {str(e)}"}

    finally:
        return {"statusCode": status_code, "body": json.dumps(body), "success": success}
