""" this module is responsible for starting the authentication passwordless process """

import json
import os

import boto3
from botocore.exceptions import ClientError

cognito_client = boto3.client("cognito-idp", region_name="us-east-1")


def lambda_handler(event, context):
    """
    send request to cognito to start the authentication process
    """
    body = json.loads(event["body"])
    user_email = body["email"]
    client_id = os.environ["COGNITO_CLIENT_ID"]

    try:
        response = cognito_client.initiate_auth(
            AuthFlow="CUSTOM_AUTH", AuthParameters={"USERNAME": user_email}, ClientId=client_id
        )
        session = response["Session"]
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "OTP enviado correctamente al correo electrónico.", "session": session}
            ),
        }
    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Error al iniciar la autenticación: {error_message}"}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Unexpected error: {str(e)}"})}
